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
        Bạn là một chuyên gia phân tích input tuyển dụng.
        Xác định input dưới đây là:
        - 'job_title' nếu input nhắm tới tên nghề/ngành công việc
        - 'skill_list' nếu input liệt kê các kỹ năng
        Chỉ trả về một từ 'job_title' hoặc 'skill_list'.
        Input: {user_input}
        """
        result = self.llm.predict(prompt)
        return result.strip().lower()
