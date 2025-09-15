import os
from dotenv import load_dotenv
from github import Github
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool

# Load biến môi trường
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Kết nối GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo("hoivd/facebook_scraper")  # thay bằng repo bạn muốn

# === Định nghĩa tool cho Agent ===
def read_file(path: str) -> str:
    """Đọc nội dung một file từ repo GitHub"""
    try:
        file_content = repo.get_contents(path)
        return file_content.decoded_content.decode("utf-8")
    except Exception as e:
        return f"Lỗi khi đọc file {path}: {e}"

def list_files(path: str = "") -> str:
    """Liệt kê file/folder trong repo GitHub"""
    try:
        contents = repo.get_contents(path)
        return "\n".join([c.path for c in contents])
    except Exception as e:
        return f"Lỗi khi liệt kê file {path}: {e}"

tools = [
    Tool(
        name="ReadFile",
        func=read_file,
        description="Dùng để đọc nội dung file từ repo. Input là đường dẫn file, ví dụ: README.md"
    ),
    Tool(
        name="ListFiles",
        func=list_files,
        description="Dùng để liệt kê file/folder trong repo. Input là đường dẫn folder, ví dụ: '' (root) hoặc 'src'"
    ),
]

# === Khởi tạo Gemini LLM ===
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=GOOGLE_API_KEY
)

# === Khởi tạo Agent ===
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# === Test hỏi đáp ===
agent.run("Hãy đọc file README.md và tóm tắt nội dung cho tôi.")