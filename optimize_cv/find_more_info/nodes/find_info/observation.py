class ObservationNode:
    def __call__(self, state):
        new_entry = {
            # "CoT": state.get("reAct", {}).get("cot"),
            "thought": state.get("reAct", {}).get("thought"),
            "action": state.get("reAct", {}).get("action"),
            "observation": state.get("reAct", {}).get("observation"),
        }
        history = state.get("history", [])
        history = history + [new_entry]   # append an toàn
        return {"history": history, 'current_step': 'observation_node'}