import os
from utils import Utils
from logger import _setup_logger

# Lấy config và logger
config = Utils.get_config()
logger = _setup_logger(__name__, level=config["logging"]["level"])


class PromptManager:
    def __init__(self, base_dir="prompts"):
        self.base_dir = base_dir
        logger.info(f"✅ PromptManager khởi tạo (base_dir='{self.base_dir}')")

    def load(self, name: str) -> str:
        path = os.path.join(self.base_dir, f"{name}.txt")
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                logger.info(f"📄 Đã load prompt '{name}' từ {path}")
                logger.debug(f"Nội dung prompt:\n{content}")
                return content
        except FileNotFoundError:
            logger.error(f"❌ Prompt file không tồn tại: {path}")
            raise

    def render(self, name: str, **kwargs) -> str:
        template = self.load(name)
        rendered = template.format(**kwargs)
        logger.info(f"✨ Prompt '{name}' đã render thành công")
        logger.debug(f"Nội dung render:\n{rendered}")
        return rendered


def main():
    pm = PromptManager()

    # Ví dụ: file prompts/jd_extraction.txt có nội dung:
    # "Trích xuất JD sau thành JSON:\n{jd_text}"
    jd_text = "ABBANK tuyển AI Architect, yêu cầu Python, Docker, Microservices."
    prompt = pm.render("jd_extraction", jd=jd_text)

    print("==== Prompt Rendered ====")
    print(prompt)


if __name__ == "__main__":
    main()