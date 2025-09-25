from langchain.agents import initialize_agent, Tool
from agent.tools.github.github_tool import GithubTool
from agent.tools.neo4j.neo4j_tool import Neo4jTool
from agent.tools.stop_tool import stop_conversation
from config.settings import Settings
from langchain_google_genai import ChatGoogleGenerativeAI
from.memory import get_memory
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class ConversationalAgent:
    def __init__(self):
        self.github_tool = GithubTool()
        self.neo4j_tool = Neo4jTool()
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            google_api_key = Settings.GOOGLE_API_KEY
        )
        
        self.memory = get_memory()
        
        tools = [
            Tool(
                name="ReadFile",
                func=self.github_tool.read_file,
                description="Đọc nội dung file trong repo. Input là tên file, ví dụ: README.md"
            ),
            Tool(
                name="ListFiles",
                func=self.github_tool.list_files,
                description="Liệt kê file/folder trong repo. Input là thư mục, ví dụ: Nếu thư mục gốc thì là '/' hoặc 'src'"
            ),
            Tool(
                name="StopConversation",
                func=stop_conversation,
                description="Dùng khi người dùng nói cảm ơn, muốn dừng, thoát hoặc kết thúc hội thoại."
            ),
            Tool(
                name="GenerateCypherQuery",
                func=self.neo4j_tool.generate_cypher,
                description="Dùng để sinh câu lệnh Cypher từ ngôn ngữ tự nhiên. Input là prompt của người dùng, output là query Cypher."
            ),
            Tool(
                name="RunCypherQuery",
                func=self.neo4j_tool.run_cypher,
                description="Dùng để chạy câu lệnh Cypher trực tiếp trên Neo4j DB. Input là query Cypher."
            )
        ]
        
        self.agent = initialize_agent(
            tools,
            self.llm,
            agent="conversational-react-description",
            memory=self.memory,
            verbose=False
        )
        
    def chat(self, user_input: str) -> str:
        response = self.agent.invoke({"input": user_input})
        return response['output']