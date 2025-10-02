# agent/tools/neo4j/detect_input_tool.py
from langchain.agents import Tool

class DetectInputTypeTool:
    """
    Dùng LLM để detect xem input là:
    - JobTitle
    - List[Skill]
    - Question (câu hỏi mở)
    """
    def __init__(self, llm):
        self.llm = llm

    def detect(self, user_input: str) -> str:
        prompt = f"""
        Bạn là chuyên gia phân loại input tuyển dụng.
        Nhiệm vụ: xác định loại input mà người dùng nhập vào.

        Quy tắc:
        - Nếu input nói về một công việc, trả về 'job_title'.
        - Nếu input liệt kê kỹ năng (A, B, C), trả về 'skill_list'.
        - Nếu input là câu hỏi mở, hỏi thông tin về job, công ty, skill,... trả về 'question'.

        Lưu ý:
        - Chỉ trả về một trong ba từ: 'job_title', 'skill_list', 'question'.
        - KHÔNG giải thích thêm.

        Input: {user_input}
        """
        result = self.llm.predict(prompt)
        return result.strip().lower()



