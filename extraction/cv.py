import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from extractor import Extractor
from logger import _setup_logger
from utils import Utils
import re 
import json
from typing import Optional


# Lấy config & logger
config = Utils.get_config()
logger = _setup_logger(__name__, level=config["logging"]["level"])


class CVExtractor(Extractor):
    def __init__(self, gemini_manager, prompt_manager, neo4j_driver, debug = True, data_dir = "debug"):
        
        super().__init__(gemini_manager, prompt_manager, neo4j_driver)
        self.debug = debug
        self.data_dir = data_dir

    def PDF2Json(self, pdf_path: str) -> Optional[dict]:
        """
        Đọc CV từ PDF, gọi Gemini để phân tích và trả về JSON (dict).
        """
        def extract_json(text: str) -> Optional[str]:
            pattern = r"```json\s*(\{.*?\})\s*```"
            match = re.search(pattern, text, re.DOTALL)
            return match.group(1) if match else None
        
        try:
            # load prompt CV extractor
            prompt = self.prompt_manager.load("cv_extractor")

            # gọi Gemini với PDF + prompt
            reps = self.gemini_manager.generate_from_pdf(pdf_path, prompt)

            # parse kết quả JSON
            json_str = extract_json(reps)
            if not json_str:
                logger.error("❌ Không tìm thấy JSON trong phản hồi Gemini")
                return None

            # Convert sang dict
            json_obj = json.loads(json_str)

            if self.debug:
                os.makedirs(self.data_dir, exist_ok=True)
                debug_file = os.path.join(self.data_dir, "cv_extracted.json")
                with open(debug_file, "w", encoding="utf-8") as f:
                    json.dump(json_obj, f, ensure_ascii=False, indent=2)
                print(f"💾 Đã lưu debug JSON tại: {debug_file}")

            return json_obj

        except json.JSONDecodeError as e:
            logger.error(f"❌ Lỗi parse JSON từ Gemini: {e}")
            logger.debug(f"Nội dung trả về:\n{json_obj}")
            return None
        except Exception as e:
            logger.error(f"❌ Lỗi khi xử lý PDF2Json: {e}")
            return None

    def Text2Json(self, jd_text: str) -> Optional[dict]:
        pass

if __name__ == "__main__":
    from gemini_llm import GeminiLLM
    from prompt_manager import PromptManager
    from cypher.cleaner import Neo4jCleaner
    from cypher.cypher_manager import Neo4jDriver

    delete_db = False
    gm = GeminiLLM()
    pm = PromptManager()
    with Neo4jDriver() as neo_driver:
        if delete_db:
            Neo4jCleaner.delete_all(neo_driver)
        

        app = CVExtractor(gm, pm, neo_driver, debug=True)

        cv_path1 = 'data/cv_pdhh.pdf'
        cv_path2 = 'data/cv_hoivd.pdf'
        app.extract_pdf(cv_path1)
        app.extract_pdf(cv_path2)