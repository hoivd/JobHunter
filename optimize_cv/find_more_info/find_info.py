from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools.git_tools import GitHubToolsManager
from .tools.ask_user_tools import AskUserToolsManager
from .tools.tool_manager_registry import ToolManagerRegistry
import json
from .nodes.find_info.next_mission import NextMissionNode
from .nodes.find_info.observation import ObservationNode
from .nodes.find_info.tool_node import ToolNode
from .nodes.find_info.plan_node import PlanningNode
from .nodes.find_info.generate_slot import GenerateSlotNode
from .nodes.find_info.parse_plan import ParsePlanNode
from typing import TypedDict, List, Dict, Any
import re

class State(TypedDict):
    plan_result: str
    missions: List[Dict[str, Any]]
    mission_index: int
    current_mission: Dict[str, Any]
    collected_info: Dict[str, Any]
    history: List[Dict[str, Any]]
    reAct: dict
    tool_outputs: List[Dict[str, Any]]
    end_mission: bool
    current_step: str

class Router:
    @staticmethod
    def route(state):
        current_step = state['current_step']

        if current_step == "tool_node":
            return "observation_node"

        elif current_step == "observation_node":
            print(f"end_mission: {state['end_mission']}")
            if state["end_mission"] == True:
                
                return "next_mission"
            else:
                return "planning_node"

        elif current_step == "next_mission":
            return "generate_slots" if state['mission_index'] <= len(state['missions']) != "END" else "END"

        return "END"

class MissionAgentSystem:
    def __init__(self, llm):
        self.llm = llm
        self.tools_manager = ToolManagerRegistry([
            GitHubToolsManager(),
            AskUserToolsManager(),
        ])
        
        self.workflow = StateGraph(State)

        # Thêm node
        self.workflow.add_node("parse_plan", ParsePlanNode())
        self.workflow.add_node("generate_slots", GenerateSlotNode(llm))
        self.workflow.add_node("planning_node", PlanningNode(llm, self.tools_manager))
        self.workflow.add_node("tool_node", ToolNode(self.tools_manager))
        self.workflow.add_node("observation_node", ObservationNode())
        self.workflow.add_node("next_mission", NextMissionNode())

        # Entry
        self.workflow.set_entry_point("parse_plan")

        # Edge
        self.workflow.add_edge("parse_plan", "generate_slots")
        self.workflow.add_edge("generate_slots", "planning_node")
        self.workflow.add_edge("planning_node",  "tool_node")
        self.workflow.add_conditional_edges("tool_node", Router.route, "observation_node: observation_node")

        # Conditional edge: evaluation → router
        self.workflow.add_conditional_edges(
            "observation_node",
            Router.route,
            {"planning_node": "planning_node", "next_mission": "next_mission"},
        )

        # Conditional edge: next_mission → router
        self.workflow.add_conditional_edges(
            "next_mission",
            Router.route,
            {"generate_slots": "generate_slots", "END": END},
        )

        self.app = self.workflow.compile()

    def run(self, plan_result: str):
        state: State = {
            "plan_result": plan_result,
            "missions": [],
            "mission_index": 0,
            "current_mission": {},
            "collected_info": [],
            "planning": "",
            "tool_outputs": [],
            "evaluation": "",
            "history": [],
            "end_mission": False,
            "current_step": "parse_plan",
        }
        return self.app.invoke(state, config={"recursion_limit": 1000})
    

class MissionAgentNode:
    def __init__(self, llm):
        self.agent = MissionAgentSystem(llm)  # Agent con

    def __call__(self, state):
        # state ở graph cha có thể chứa thông tin cần truyền cho agent con
        plan_result = state.get("plan_result", "")
        print(plan_result)
        print(type(plan_result))
        def extract_json_from_codeblock(text: str):
            """
            Trích xuất JSON từ block ```json ... ``` trong chuỗi text.
            Trả về dict (hoặc list) nếu parse được, ngược lại trả về None.
            """
            pattern = r"```json\s*(.*?)\s*```"
            match = re.search(pattern, text, re.DOTALL)

            if not match:
                return None

            json_str = match.group(1)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print("❌ Lỗi parse JSON:", e)
                return None
        json_plan = extract_json_from_codeblock(plan_result)

        # Gọi agent con
        final_state = self.agent.run(json_plan)

        # Trả dữ liệu cần thiết về cho graph cha
        state["mission_final_state"] = final_state
        return state
    
def main():

    from dotenv import load_dotenv
    import os
    import json
    
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0,
            api_key=api_key,
        )
    with open("find_more_info/plan.json", "r", encoding="utf-8") as f:
        plan_result = f.read()

    system = MissionAgentSystem(llm)
    final_state = system.run(plan_result)

    print("\n=== FINAL STATE ===")
    print(final_state)

if __name__ == "__main__":
    main()
