from langchain.tools import tool
from .base_tools import BaseToolsManager  # lớp cha bạn đã có


class AskUserToolsManager(BaseToolsManager):
    def _build_tools(self):
        @tool("ask_user")
        def ask_user(question: str) -> str:
            """Hỏi trực tiếp người dùng một câu hỏi và trả về câu trả lời."""
            try:
                print(f"👉 {question}")
                answer = input("Trả lời: ")
                return answer.strip()
            except Exception as e:
                return f"Error: {e}"

        return {'ask_user': ask_user}


if __name__ == "__main__":
    manager = AskUserToolsManager()
    print("📌 Tools text:\n")
    print(manager.get_tools_text())

    # Test chạy tool
    tool = manager.get_tools()['ask_user']
    result = tool.invoke("Bạn có thể cho tôi biết kỹ năng chính của bạn là gì?")
    print("✅ Result:", result)