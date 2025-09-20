from extractor import Extractor

class JDExtractor(Extractor):
    def __init__(self, gemini_manager, prompt_manager, neo4j_driver, debug = False, data_dir = "debug"):
        
        super().__init__(gemini_manager, prompt_manager, neo4j_driver)