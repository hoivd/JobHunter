import sys
import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logger import _setup_logger
from utils import Utils


config = Utils.get_config()
logger = _setup_logger(__name__, level=config["logging"]["level"])

from utils import Utils

class Neo4jQueryRunner:
    """
    Lớp chạy query trên Neo4j, bọc ngoài driver với logging.
    """

    def __init__(self, driver):
        self.driver = driver

    def run(self, query: str, params: dict = None):
        """Thực thi query và log kết quả."""
        try:
            logger.debug(f"▶️ Query:\n{query}\nParams: {params}")
            query = Utils.extract_cypher(query)
            result = self.driver.run_query(query, params or {})
            

            # Nếu driver trả về list[dict]
            records = result if isinstance(result, list) else [r.data() for r in result]

            logger.info(f"✅ Query chạy thành công, số bản ghi: {len(records)}")
            return records
        except Exception as e:
            logger.error(f"❌ Lỗi khi chạy query: {e}")
            # return {"error": str(e)}
            raise