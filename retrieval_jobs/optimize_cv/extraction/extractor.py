# jd_extraction_app.py
from logger import _setup_logger
from utils import Utils
import re
import json
from typing import Optional
from abc import ABC, abstractmethod


# Import thêm
from cypher.generate_code.json2cypher import Json2Cypher
from cypher.cypher_manager import Neo4jDriver

# Lấy config & logger
config = Utils.get_config()
logger = _setup_logger(__name__, level=config["logging"]["level"])


class Extractor(ABC):
    def __init__(self, 
                 gemini_manager,
                 prompt_manager,
                 neo4j_driver, 
                 debug: bool = False, 
                 data_dir: str = "debug"):
        self.gemini_manager = gemini_manager
        self.prompt_manager = prompt_manager
        self.neo4j_driver = neo4j_driver
        self.debug = debug
        self.data_dir = data_dir
        logger.info("✅ JDExtractorApp đã khởi tạo")

    @abstractmethod
    def Text2Json(self, text: str) -> Optional[dict]:
        pass

    @abstractmethod
    def PDF2Json(self, pdf_path: str) -> Optional[dict]:
        pass

    def Json2DB(self, json_obj: dict):
        """
        Nhận JSON (dict), sinh Cypher bằng Json2Cypher rồi insert vào Neo4j.
        """
        try:
            logger.info("🚀 Bắt đầu chuyển JSON sang Cypher script")

            converter = Json2Cypher(json_obj)
            cypher_script = converter.to_cypher()
            converter.save("debug/cyphers/job.cypher")

            logger.debug(f"📜 Cypher script:\n{cypher_script}")

            self.neo4j_driver.run_query(cypher_script)

            logger.info("✅ JSON đã được ghi vào Neo4j thành công")

        except Exception as e:
            logger.error(f"❌ Lỗi khi Json2DB: {e}")
            raise
    
    def extract_text(self, text: str):
        json_obj = self.Text2Json(text)
        if json_obj:
            self.Json2DB(json_obj)

    def extract_pdf(self, pdf_path: str):
        json_obj = self.PDF2Json(pdf_path)
        if json_obj:
            self.Json2DB(json_obj)



