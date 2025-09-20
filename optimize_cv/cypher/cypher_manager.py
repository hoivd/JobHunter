from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

class Neo4jDriver:
    def __init__(self):
        # load biến môi trường
        load_dotenv()
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")

        if not all([uri, user, password]):
            raise ValueError("❌ Thiếu NEO4J_URI, NEO4J_USERNAME hoặc NEO4J_PASSWORD trong .env")

        # khởi tạo driver
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print("✅ Kết nối Neo4j thành công.")

    def close(self):
        if self.driver:
            self.driver.close()
            print("🔌 Driver Neo4j đã được đóng.")

    def run_query(self, query: str, parameters: dict = None):
        """Thực thi query Cypher"""
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


# ===== Ví dụ sử dụng =====
if __name__ == "__main__":
    with Neo4jDriver() as db:
        q = "RETURN 'Hello Neo4j' AS msg"
        res = db.run_query(q)
        print(res)