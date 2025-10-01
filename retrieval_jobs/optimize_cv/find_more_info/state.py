from typing import TypedDict, Literal
from fastapi import WebSocket


class State(TypedDict):
    cv_info: str
    jd_info: str
    jd_extracted: str
    analysis_result: str
    plan_result: str
    mission_final_state = dict
    completed_cv: str
    current_step: Literal[
        "agent_jd_extraction",
        "agent_analysis_per_info",
        "agent_plan_find_info",
        "END"
    ]