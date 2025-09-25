from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import Settings
from .graph_schema import GRAPH_SCHEMA

class CypherGenerator:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        google_api_key=Settings.GOOGLE_API_KEY
    )
    def generate(self, prompt: str) -> str:
        try:
            query = self.llm.predict(
                f"""
                Bạn là chuyên gia Neo4j Cypher.
                Nhiệm vụ:
                1. Đầu tiên, phân tích schema để xác định đường đi từ các node/relationship có sẵn.
                2. Chỉ chọn các quan hệ và node KHỚP CHÍNH XÁC với schema sau (không tự bịa thêm).
                3. Sau khi phân tích, sinh ra Cypher query hợp lệ.

                Schema GraphDB:
                {GRAPH_SCHEMA}

                Ví dụ cách làm:
                - User prompt: "Tìm kiếm các công ty yêu cầu skill Python"
                - Phân tích: Company → JD (CompanyPublishesJD / JDBelongsToCompany), JD → Skills (JDRequiresSkills), Skills → Skill (CONTAINS)
                - Query:
                MATCH (c:Company)-[:CompanyPublishesJD]->(jd:JD)-[:JDRequiresSkills]->(skills:Skills)-[:CONTAINS]->(skill:Skill {{name:"Python"}})
                RETURN DISTINCT c.name

                Yêu cầu người dùng: {prompt}

                Trả về:
                - Chỉ Cypher query hợp lệ, KHÔNG giải thích thêm.
                """
            )
            return query.strip()
        except Exception as e:
            return f"Lỗi khi sinh Cypher: {e}"