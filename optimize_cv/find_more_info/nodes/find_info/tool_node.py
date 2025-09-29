import re
import json


class ToolNode:
    """
    Node thực thi Action mà LLM sinh ra trong ReAct loop.
    Action dạng: ToolName[input]
    Ví dụ:
    - ask_user[{"question": "What is your name?"}]
    - github_get_user_pygithub[{"username": "torvalds"}]
    - End[{...json kết quả...}]
    """

    def __init__(self, tool_registry):
        """
        - tool_registry: instance của ToolManagerRegistry
        """
        self.registry = tool_registry

    def __call__(self, state: dict):
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
            collected_info = state["collected_info"] + [result] 
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

        if not tool_func:
            print(f"⚠️ Tool '{tool_name}' không tồn tại trong registry")
            observation = {"error": f"Tool '{tool_name}' không tồn tại"}
        else:
            try:
                if tool_input and tool_input.startswith("{"):
                    parsed_input = json.loads(tool_input)
                    observation = tool_func.invoke(parsed_input)
                elif tool_input:
                    observation = tool_func.invoke(tool_input)
                else:
                    observation = tool_func.invoke({})
            except Exception as e:
                observation = {"error": str(e)}

        # --- Ghi vào state ---
        # state["reAct"]["cot"] = cot
        state["reAct"]["thought"] = reason
        state["reAct"]["action"] = action
        if tool_name == "ask_user":
            state["reAct"]["observation"] = "HumanInput: " + observation
        else:
            state["reAct"]["observation"] = observation


        return {"current_step": "tool_node"}
    
if __name__ == "__main__":
    # Import ở đây để chỉ dùng khi test
    from ...tools.tool_manager_registry import ToolManagerRegistry
    from ...tools.git_tools import GitHubToolsManager
    from ...tools.ask_user_tools import AskUserToolsManager

    # Tạo registry và đăng ký managers
    registry = ToolManagerRegistry()
    registry.register_manager(GitHubToolsManager())
    registry.register_manager(AskUserToolsManager())

    # Khởi tạo ToolNode với registry
    node = ToolNode(registry)

    # State mẫu để test
    state = {
        "reAct": {
            "goal": "Hoàn thiện phần thông tin cá nhân theo yêu cầu của CV chuyên nghiệp.",
            "objective": "Thu thập đầy đủ các thông tin sau: Họ và tên đầy đủ, Số điện thoại, Địa chỉ email chuyên nghiệp, Địa chỉ (thành phố/tỉnh), Liên kết LinkedIn (nếu có), Liên kết GitHub (rất quan trọng).",
            "raw_response": "**CoT**: Objective là thu thập thông tin cá nhân chi tiết cho CV, bao gồm Họ và tên đầy đủ, Số điện thoại, Địa chỉ email chuyên nghiệp, Địa chỉ (thành phố/tỉnh), Liên kết LinkedIn, và Liên kết GitHub. Hiện tại chưa có bất kỳ thông tin nào. Để bắt đầu, tôi cần hỏi ứng viên về các thông tin cơ bản này. Công cụ `ask_user` là phù hợp nhất để thu thập thông tin trực tiếp từ ứng viên. Tôi sẽ bắt đầu bằng việc hỏi họ và tên đầy đủ.\n**Reason**: Cần thu thập thông tin cá nhân cơ bản từ ứng viên để hoàn thiện CV.\n**Action**: ask_user[{\"question\": \"Vui lòng cung cấp họ và tên đầy đủ của bạn.\"}]",
            "action_line": "**Action**: ask_user[{\"question\": \"Vui lòng cung cấp họ và tên đầy đủ của bạn.\"}]"
        },
        "current_step": "planning_node"
    }

    # Chạy ToolNode
    result = node(state)

    print("\n=== State sau khi chạy ToolNode ===")
    print(json.dumps(state, ensure_ascii=False, indent=2))
    print("\n=== Kết quả return ===")
    print(result)