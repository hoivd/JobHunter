import logging
import os
import sys
from datetime import datetime


def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def _setup_logger(name: str, level: str = "INFO", log_file: str = None) -> logging.Logger:
    """
    Khởi tạo và trả về logger đã cấu hình:
    - Hỗ trợ level dạng string: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL".
    - Ghi ra console (stdout).
    - Ghi ra file log ./log/app_YYYY-MM-DD_HH-MM-SS.log với UTF-8 (nếu không truyền log_file).
    - Tự động tạo thư mục log nếu chưa tồn tại.
    """
    # Convert string level -> logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Nếu không truyền log_file thì dùng mặc định theo timestamp
    if log_file is None:
        log_file = f'./log/app_{get_current_timestamp()}.txt'

    formatter = logging.Formatter("<%(levelname)s-%(name)s> - %(message)s")

    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)
    logger.propagate = False  # Không lặp log nếu dùng root logger

    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Đảm bảo thư mục log tồn tại
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # File handler UTF-8
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    logger = _setup_logger("main", level="ERROR", log_file="main.log")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
