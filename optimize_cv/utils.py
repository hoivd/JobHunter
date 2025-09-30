import yaml
from functools import lru_cache
import os
import json
from datetime import datetime

class Utils:
    @staticmethod
    @lru_cache
    def get_config(path: str = "D:\JobHunter\optimize_cv\config.yaml") -> dict:
        """
        Đọc file YAML config và cache lại để không phải đọc nhiều lần.
        Trả về dict Python.
        """
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
        
    @staticmethod
    def save_json(data: dict, filename: str, dir_path: str = "data", timestamp: bool = True) -> str:
        os.makedirs(dir_path, exist_ok=True)
        if timestamp:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename}_{ts}.json"
        else:
            filename = f"{filename}.json"

        file_path = os.path.join(dir_path, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return file_path

    @staticmethod
    def read_json(path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def json_to_str(data: dict) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def str_to_json(s: str) -> dict:
        return json.loads(s)
        
def main():
    config = Utils.get_config()
    print(config)

if __name__ == "__main__":
    main()