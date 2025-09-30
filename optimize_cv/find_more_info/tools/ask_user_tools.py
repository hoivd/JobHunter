from langchain.tools import tool
from .base_tools import BaseToolsManager  # lớp cha bạn đã có
from fastapi import WebSocket
import asyncio


class AskUserToolsManager(BaseToolsManager):
    def _build_tools(self):
        @tool("ask_user")
        async def ask_user(question: str, ws = None) -> str:
            """Hỏi trực tiếp người dùng một câu hỏi và trả về câu trả lời."""
            try:
                print(f"👉 {question}")
                print(ws)
                if ws:  # hỏi qua WebSocket
                    await ws.send_text(str(question))
                    answer = await ws.receive_text()
                    return answer.strip()
                else:   # fallback: terminal
                    answer = input("Trả lời: ")
                    return answer.strip()
            except Exception as e:
                return f"Error: {e}"

        return {'ask_user': ask_user}

async def main():
    manager = AskUserToolsManager()
    print("📌 Tools text:\n")
    print(manager.get_tools_text())

    # Test chạy tool
    tool = manager.get_tools()['ask_user']
    result = await tool.invoke({
        "question": "Bạn có thể cho tôi biết kỹ năng chính của bạn là gì?"
    })
    print("✅ Result:", result)

if __name__ == "__main__":
    asyncio.run(main())