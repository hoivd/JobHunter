from langchain.agents import initialize_agent, Tool
from agent.tools.github.github_tool import GithubTool
from agent.tools.neo4j.neo4j_tool import Neo4jTool
from agent.tools.stop_tool import stop_conversation
from config.settings import Settings
from langchain_google_genai import ChatGoogleGenerativeAI
from agent.tools.neo4j.detect_input_tool import DetectInputTypeTool
from .memory import get_memory
import json
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from retrieval.retriever import JobRetriever
class ConversationalAgent:
    def __init__(self):
        self.github_tool = GithubTool()
        self.neo4j_tool = Neo4jTool()
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            google_api_key=Settings.GOOGLE_API_KEY
        )
        
        self.memory = get_memory()

        self.detect_tool = DetectInputTypeTool(self.llm)
        
        # Tool dùng LLM để detect input
        self.detect_tool = DetectInputTypeTool(self.llm)

        tools = [
            Tool(
                name="ReadFile",
                func=self.github_tool.read_file,
                description="Đọc nội dung file trong repo. Input là tên file, ví dụ: README.md"
            ),
            Tool(
                name="ListFiles",
                func=self.github_tool.list_files,
                description="Liệt kê file/folder trong repo."
            ),
            Tool(
                name="StopConversation",
                func=stop_conversation,
                description="Dùng khi người dùng muốn dừng hội thoại."
            ),
            Tool(
                name="GenerateCypherQuery",
                func=self.neo4j_tool.generate_cypher,
                description="Sinh câu lệnh Cypher từ ngôn ngữ tự nhiên."
            ),
            Tool(
                name="RunCypherQuery",
                func=self.neo4j_tool.run_cypher,
                description="Chạy câu lệnh Cypher trực tiếp trên Neo4j DB."
            )
        ]
        
        self.agent = initialize_agent(
            tools,
            self.llm,
            agent="conversational-react-description",
            memory=self.memory,
            verbose=False
        )
        
    def chat(self, user_input: str, top_k: int = 5) -> dict:
        """
        Nhận input tự nhiên (JobTitle hoặc Skill list), trả về JSON:
        {'jobs': [...], 'jd_details': [...]}
        """
        # Bước 1: Dùng agent/LLM detect input type
        input_type = self.detect_tool.detect(user_input)

        retriever = JobRetriever()
        retriever.load_index()
    
        jobs = []

        # Bước 2: Lấy top K jobs
        if input_type == "job_title":
            jobs = retriever.get_similar_jobs(user_input, top_k=top_k)
        elif input_type == "skill_list":
            # Parse skill list từ input (dùng ast.literal_eval nếu có, fallback split ',')
            import ast
            try:
                skills = ast.literal_eval(user_input)
                if not isinstance(skills, list):
                    skills = [user_input]
            except:
                skills = [s.strip() for s in user_input.split(",")]
            jobs = retriever.get_jobs_from_skills(skills, top_k=top_k)
        else:
            return {"error": "Không xác định được JobTitle hoặc danh sách Skill."}

        # Bước 3: Lấy JD chi tiết
        jd_details = []
        print(jobs)
        for job in jobs:
            cypher_query = f"""
            MATCH (jt:JobTitle {{name: '{job}'}})-[:JobTitleDescribesJD]->(jd:JD)
            OPTIONAL MATCH (jd)-[:JDBelongsToCompany]->(c:Company)
            OPTIONAL MATCH (jd)-[:JDRequiresDegrees]->(d:Degrees)-[:CONTAINS]->(deg:Degree)
            OPTIONAL MATCH (jd)-[:JDRequiresSkills]->(s:Skills)-[:CONTAINS]->(skill:Skill)
            OPTIONAL MATCH (jd)-[:JDDescribesTasks]->(t:Tasks)-[:CONTAINS]->(task:Task)
            OPTIONAL MATCH (jd)-[:JDProvidesBenefits]->(b:Benefits)-[:CONTAINS]->(benefit:Benefit)
            RETURN jd.name AS JD_Name,
                jd.mode AS JD_Mode,
                c.name AS Company_Name,
                c.mode AS Company_Mode,
                c.country AS Company_Country,
                c.size AS Company_Size,
                c.industry AS Company_Industry,
                c.id_image AS Company_Image,
                collect(DISTINCT deg.name) AS Degrees,
                collect(DISTINCT skill.name) AS Skills,
                collect(DISTINCT task.name) AS Tasks,
                collect(DISTINCT benefit.name) AS Benefits
            """
            jd_info = self.neo4j_tool.run_cypher(cypher_query)
            jd_details.append({job: jd_info})

        with open("output/jd_details.json", "w", encoding="utf-8") as f:
            json.dump(jd_details, f, ensure_ascii=False, indent=4)

        return {"jobs": jobs, "jd_details": jd_details}

if __name__ == "__main__":
    agent = ConversationalAgent()
    print("Chào mừng bạn đến với Conversational Agent! Gõ 'exit' để thoát.")

    while True:
        user_input = input("Bạn: ")
        if user_input.lower() in ["exit", "quit", "thoát"]:
            print("Agent: Hẹn gặp lại!")
            break
        try:
            response = agent.chat(user_input)
            print(f"Agent: {response}")
        except Exception as e:
            print(f"Agent gặp lỗi: {e}")
