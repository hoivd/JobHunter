import yaml
from functools import lru_cache

class Utils:
    @staticmethod
    @lru_cache
    def get_config(path: str = "config.yaml") -> dict:
        """
        Đọc file YAML config và cache lại để không phải đọc nhiều lần.
        Trả về dict Python.
        """
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
        
def main():
    config = Utils.get_config()
    print(config)

if __name__ == "__main__":
    main()