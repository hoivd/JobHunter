import sys

def stop_conversation(_: str = "") -> str:
    """Dừng cuộc trò chuyện khi người dùng muốn thoát"""
    print("🤖 Agent: Cảm ơn bạn, mình sẽ dừng ở đây 👋")
    sys.exit(0)