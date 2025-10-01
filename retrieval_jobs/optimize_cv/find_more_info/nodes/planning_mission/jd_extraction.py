from ...state import State

class AgentJDExtraction:
    """Agent 1: Trích xuất yêu cầu từ JD"""
    def __init__(self, llm):
        self.llm = llm

    def __call__(self, state: State):
        prompt = f"""
        Bạn là một chuyên gia phân tích Job Description. 
        Nhiệm vụ: Đọc và phân tích thông tin Job Description mà người dùng cung cấp, sau đó trích xuất các thông tin chính theo cấu trúc sau:

        1. Chức danh công việc:
        2. Mô tả công việc (nhiệm vụ chính):
        3. Yêu cầu bắt buộc (kỹ năng, kinh nghiệm, học vấn):
        4. Kỹ năng/kinh nghiệm ưu tiên (nếu có):
        5. Quyền lợi / phúc lợi:
        6. Địa điểm / Hình thức làm việc:

        Đây là Job Description cần phân tích:
        {state['jd_info']}
        """
        print("\n=== Agent JD Extraction ===")
        result = self.llm.invoke(prompt).content
        print("Output từ LLM:\n", result)
        state["jd_extracted"] = result
        return {"jd_extracted": result, "current_step": "agent_jd_extraction"}