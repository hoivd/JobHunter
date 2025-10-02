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
import json
from agent.tools.neo4j.cypher_generator import CypherGenerator
import ast

def parse_jd_details(data):
    parsed_data = {}
    for key, value in data[0].items():
        try:
            # Use ast.literal_eval instead of json.loads
            parsed_data[key] = ast.literal_eval(value)
        except Exception as e:
            print(f"Error parsing {key}: {e}")
            parsed_data[key] = None
    return parsed_data

class RouteQueryTool:
    def __init__(self, detect_tool, job_retriever, neo4j_tool, cypher_generator, llm):
        self.detect_tool = detect_tool
        self.job_retriever = job_retriever
        self.neo4j_tool = neo4j_tool
        self.cypher_generator = cypher_generator
        self.llm = llm

    def route(self, user_input: str, top_k: int = 5) -> dict:
        input_type = self.detect_tool.detect(user_input)

        if input_type in ["job_title", "skill_list"]:
            return self._handle_job_query(user_input, input_type, top_k)
        elif input_type == "question":
            return self._handle_rag_query(user_input)
        else:
            return {"error": "Không xác định được loại input."}

    def _handle_job_query(self, user_input, input_type, top_k):
        jobs = []
        if input_type == "job_title":
            jobs = self.job_retriever.get_similar_jobs(user_input, top_k=top_k)
        else:
            import ast
            try:
                skills = ast.literal_eval(user_input)
                if not isinstance(skills, list):
                    skills = [user_input]
            except:
                skills = [s.strip() for s in user_input.split(",")]
            jobs = self.job_retriever.get_jobs_from_skills(skills, top_k=top_k)

        jd_details = []
        for job in jobs:
            cypher_query = f"""
            ```cypher
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
            ```
            """
            jd_info = self.neo4j_tool.run_cypher(cypher_query)
            jd_details.append({job: jd_info})

        flattened_data = []

        for item in jd_details:
            parsed_item = parse_jd_details([item])
            for job_title, jobs in parsed_item.items():
                if isinstance(jobs, list):
                    for job in jobs:
                        job_copy = job.copy()
                        job_copy['job_title'] = job_title
                        flattened_data.append(job_copy)
        with open("output/jd_details.json", "w", encoding="utf-8") as f:
                json.dump(flattened_data, f, ensure_ascii=False, indent=4)

        return {"jobs": jobs, "jd_details": flattened_data}

    def _handle_rag_query(self, user_input):
        cypher_query = self.cypher_generator.generate(user_input)
        if cypher_query.startswith("Lỗi"):
            return {"error": cypher_query}

        data = self.neo4j_tool.run_cypher(cypher_query)

        llm_chatbot = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.2,
            google_api_key=Settings.GOOGLE_API_KEY
        )
        
        prompt = f"Dữ liệu truy vấn từ Neo4j: {data}\nHãy trả lời câu hỏi: {user_input}"
        answer = llm_chatbot.invoke(prompt)
        return {"answer": answer, "cypher": cypher_query, "data": data}

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

        self.job_retriever = JobRetriever()
        self.job_retriever.load_index()

        self.cypher_generator = CypherGenerator()

        # RouteQueryTool điều phối luồng xử lý
        self.router = RouteQueryTool(
            detect_tool=self.detect_tool,
            job_retriever=self.job_retriever,
            neo4j_tool=self.neo4j_tool,
            cypher_generator=self.cypher_generator,
            llm=self.llm
        )

        tools = [
            Tool(
                name="ReadFile",
                func=self.github_tool.read_file,
                description="Đọc nội dung file trong repo"
            ),
            Tool(
                name="ListFiles",
                func=self.github_tool.list_files,
                description="Liệt kê file/folder trong repo"
            ),
            Tool(
                name="StopConversation",
                func=stop_conversation,
                description="Dừng hội thoại"
            ),
            Tool(
                name="GenerateCypherQuery",
                func=self.neo4j_tool.generate_cypher,
                description="Sinh câu lệnh Cypher từ ngôn ngữ tự nhiên"
            ),
            Tool(
                name="RunCypherQuery",
                func=self.neo4j_tool.run_cypher,
                description="Chạy câu lệnh Cypher trực tiếp"
            )
        ]
        
        self.agent = initialize_agent(
            tools,
            self.llm,
            agent="conversational-react-description",
            memory=self.memory,
            verbose=True
        )
        
    def chat(self, user_input: str, top_k: int = 5) -> dict:
        return self.router.route(user_input, top_k=top_k)

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
