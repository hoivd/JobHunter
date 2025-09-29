import json

# ================= NODES =================

class ParsePlanNode:
    def __call__(self, state):
        plan = state["plan_result"]
        missions = plan.get("missions", [])
        idx = 0
        return {
            "missions": missions,
            "mission_index": idx,
            "current_mission": missions[idx] if missions else {},
            "collected_info": [],
            "current_step": "parse_plan",
        }
