class NextMissionNode:
    def __call__(self, state):
        idx = state["mission_index"] + 1
        if idx < len(state["missions"]):
            print(f"\n➡️  Chuyển sang mission tiếp theo: {state['missions'][idx]['name']}")
            print(f"collected_info: {state['collected_info']}")

            return {
                "mission_index": idx,
                "end_mission": False,
                "current_mission": state["missions"][idx],
                "current_step": "next_mission",
                'history': [], 
                'reAct': {}
            }
        else:
            print("\n✅ Hoàn thành toàn bộ mission.")
            print(f"collected_info: {state['collected_info']}")

            return {"current_step": "END", 'history': [], 'reAct': {}}