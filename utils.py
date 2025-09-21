import re
from typing import Optional
import yaml
from functools import lru_cache
import os
import json
from datetime import datetime

class Utils:
    @staticmethod
    @lru_cache
    def get_config(path: str = "config/config.yaml") -> dict:
        """
        Đọc file YAML config và cache lại để không phải đọc nhiều lần.
        Trả về dict Python.
        """
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
        
    @staticmethod
    def extract_cypher(text: str) -> Optional[str]:
        pattern = r"```cypher\s*(.*?)\s*```"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1) if match else None