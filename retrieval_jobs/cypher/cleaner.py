import sys
import os

# Thêm thư mục cha vào sys.path để import module ngoài
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logger import _setup_logger
from utils import Utils


# Lấy config & logger
config = Utils.get_config()
logger = _setup_logger(__name__, level=config["logging"]["level"])


class Neo4jCleaner:
    """
    Tiện ích dọn dẹp toàn bộ dữ liệu trong Neo4j.
    """

    @staticmethod
    def delete_all(driver):
        """Xóa toàn bộ node và relationship trong database."""
        try:
            query = "MATCH (n) DETACH DELETE n"
            driver.run_query(query)
            logger.info("🗑️ Đã xóa toàn bộ node và relationship trong Neo4j")
        except Exception as e:
            logger.error(f"❌ Lỗi khi xóa database: {e}")
            raise


# ===== Demo sử dụng =====
if __name__ == "__main__":
    from cypher_manager import Neo4jDriver

    with Neo4jDriver() as db:
        Neo4jCleaner.delete_all(db)
