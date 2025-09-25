from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
from config.settings import Settings

class Neo4jDriver:
    """
    Lớp quản lý kết nối Neo4j.
    """
    def __init__(self):
        uri = Settings.NEO4J_URI
        user = Settings.NEO4J_USERNAME
        password = Settings.NEO4J_PASSWORD

        if not all([uri, user, password]):
            raise ValueError("❌ Thiếu NEO4J_URI, NEO4J_USERNAME hoặc NEO4J_PASSWORD trong .env")

        # Khởi tạo driver
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print("✅ Kết nối Neo4j thành công.")

    def close(self):
        """Đóng kết nối driver."""
        if self.driver:
            self.driver.close()
            print("🔌 Driver Neo4j đã được đóng.")

    def run_query(self, query: str, parameters: dict = None):
        """Thực thi query Cypher và trả về list[dict]."""
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
        res = db.run_query("RETURN 'Hello Neo4j' AS msg")
        print(res)
