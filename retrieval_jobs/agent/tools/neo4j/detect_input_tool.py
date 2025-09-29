# agent/tools/neo4j/detect_input_tool.py
from langchain.agents import Tool

class DetectInputTypeTool:
    """
    Dùng LLM để detect xem input là JobTitle hay List[Skill].
    """
    def __init__(self, llm):
        self.llm = llm
        self.tool = Tool(
            name="DetectInputType",
            func=self.detect,
            description="Nhận input từ người dùng, trả về 'job_title' hoặc 'skill_list'."
        )

    def detect(self, user_input: str) -> str:
        prompt = f"""
        Bạn là chuyên gia phân loại input tuyển dụng.
        Nhiệm vụ: xác định loại input mà người dùng nhập vào.

        Quy tắc:
        - Nếu input nói về một công việc, dù ngắn gọn (VD: "job_title") 
        hay nằm trong một câu dài hơn (VD: "Tôi muốn tìm việc job_title"), 
        thì trả về 'job_title'.
        - Nếu input đề cập đến các kỹ (VD: "skill A, skill B, skill C") 
        hay nằm trong một câu dài hơn (VD: Tôi có các kỹ năng A, B, C)
        thì trả về 'skill_list' (A, B, C).

        Lưu ý:
        - Chỉ trả về đúng một trong hai từ: 'job_title' hoặc 'skill_list'.
        - Không thêm giải thích.

        Input: {user_input}
        """
        result = self.llm.predict(prompt)
        return result.strip().lower()


