import re
import json
from typing import Any, Dict


class ToolNode:
    """
    Node thực thi Action mà LLM sinh ra trong ReAct loop.
    Action dạng: ToolName[input]
    Ví dụ:
    - ask_user[{"question": "What is your name?"}]
    - github_get_user_pygithub[{"username": "torvalds"}]
    - End[{...json kết quả...}]
    """

    def __init__(self, tool_registry, ws=None):
        """
        - tool_registry: instance của ToolManagerRegistry
        - ws: WebSocket (nếu có) để pass cho tool ask_user
        """
        self.registry = tool_registry
        self.ws = ws

    async def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("\n=== Tool Node ===")
        response = state.get("reAct", {}).get("raw_response", "")
        print(response)

        # --- Parse CoT, Reason và Action ---
        cot_match = re.search(r"\*\*CoT\*\*:\s*(.*)", response, re.DOTALL)
        reason_match = re.search(r"\*\*Reason\*\*:\s*(.*)", response)
        action_match = re.search(r"\*\*Action\*\*:\s*(.*)", response)

        cot = cot_match.group(1).strip() if cot_match else "(không có CoT)"
        reason = reason_match.group(1).strip() if reason_match else "(không có Reason)"
        action = action_match.group(1).strip() if action_match else ""

        print(f"🧩 CoT parse: {cot}")
        print(f"🤔 Reason parse: {reason}")
        print(f"➡️ Action parse: {action}")

        # --- Nếu là End thì kết thúc ---
        if action.startswith("End"):
            print(response)
            result = action[len("End["):-1]
            print("\n✅ Mission hoàn thành với kết quả cuối cùng:")
            collected_info = state.get("collected_info", []) + [result]
            state["reAct"]["cot"] = cot
            state["reAct"]["thought"] = reason
            state["reAct"]["action"] = action
            state["reAct"]["observation"] = result
            return {
                "collected_info": collected_info,
                "current_step": "tool_node",
                "end_mission": True,
            }

        # --- Parse Action thành tool_name + input ---
        tool_name, tool_input = None, None
        if "[" in action and action.endswith("]"):
            tool_name = action[: action.index("[")].strip()
            raw_input = action[action.index("[") + 1 : -1].strip()
            tool_input = raw_input if raw_input else None

        # --- Lấy tool từ registry ---
        tools = self.registry.get_all_tools()
        tool_func = tools.get(tool_name)

        async def run_tool(tool_name, tool_func, tool_input):
            if tool_input and isinstance(tool_input, str) and tool_input.startswith("{"):
                parsed_input = json.loads(tool_input)
            elif tool_input:
                parsed_input = tool_input
            else:
                parsed_input = {}

            # nếu tool là ask_user thì thêm ws vào input schema
            if tool_name == "ask_user" and self.ws is not None:
                if isinstance(parsed_input, dict):
                    parsed_input["ws"] = self.ws
                else:
                    parsed_input = {"ws": self.ws, "question": parsed_input}
            print(parsed_input)
            # chạy tool (phân biệt async/sync)
            if hasattr(tool_func, "ainvoke"):  # async tool
                return await tool_func.ainvoke(parsed_input)
            else:  # sync tool
                return tool_func.invoke(parsed_input)

        # --- Thực thi tool ---
        if not tool_func:
            print(f"⚠️ Tool '{tool_name}' không tồn tại trong registry")
            observation = {"error": f"Tool '{tool_name}' không tồn tại"}
        else:
            try:
                observation = await run_tool(tool_name, tool_func, tool_input)
            except Exception as e:
                observation = {"error": str(e)}

        # --- Ghi vào state ---
        state["reAct"]["thought"] = reason
        state["reAct"]["action"] = action
        if tool_name == "ask_user":
            state["reAct"]["observation"] = "HumanInput: " + str(observation)
        else:
            state["reAct"]["observation"] = observation

        return {"current_step": "tool_node"}