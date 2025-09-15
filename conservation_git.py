import os
import sys
from dotenv import load_dotenv
from github import Github
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory

# Load biến môi trường
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Kết nối GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo("hoivd/facebook_scraper")  # thay bằng repo bạn muốn

# ==== Tools GitHub ====
def read_file(path: str) -> str:
    try:
        file_content = repo.get_contents(path)
        return file_content.decoded_content.decode("utf-8")
    except Exception as e:
        return f"Lỗi khi đọc file {path}: {e}"

def list_files(path: str = "") -> str:
    try:
        contents = repo.get_contents(path)
        return "\n".join([c.path for c in contents])
    except Exception as e:
        return f"Lỗi khi liệt kê file {path}: {e}"

# ==== Tool StopConversation ====
def stop_conversation(_: str = "") -> str:
    """Dừng cuộc trò chuyện khi người dùng muốn thoát"""
    print("🤖 Agent: Cảm ơn bạn, mình sẽ dừng ở đây 👋")
    sys.exit(0)  # Thoát hẳn chương trình

tools = [
    Tool(
        name="ReadFile",
        func=read_file,
        description="Đọc nội dung file trong repo. Input là tên file, ví dụ: README.md"
    ),
    Tool(
        name="ListFiles",
        func=list_files,
        description="Liệt kê file/folder trong repo. Input là thư mục, ví dụ: Nếu thư mục gốc thì là '/' hoặc 'src'"
    ),
    Tool(
        name="StopConversation",
        func=stop_conversation,
        description="Dùng khi người dùng nói cảm ơn, muốn dừng, thoát hoặc kết thúc hội thoại."
    ),
]

# ==== LLM (Gemini) ====
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=GOOGLE_API_KEY
)

# ==== Memory ====
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# ==== Conversational Agent ====
agent = initialize_agent(
    tools,
    llm,
    agent="conversational-react-description",
    memory=memory,
    verbose=True
)

# ==== Vòng lặp hội thoại ====
print("🤖 Agent sẵn sàng! Bạn có thể chat, gõ 'cảm ơn' hay 'muốn dừng' để kết thúc.\n")

while True:
    query = input("Bạn: ")
    response = agent.run(query)
    print("🤖 Agent:", response)