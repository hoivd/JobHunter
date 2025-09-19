from dotenv import load_dotenv
import google.generativeai as genai
import os
from utils import Utils
from logger import _setup_logger

# Load config và logger
config = Utils.get_config()
logger = _setup_logger(__name__, level=config["logging"]["level"])


class GeminiManager:
    def __init__(self, model: str = "gemini-2.5-flash-lite", temperature: float = 0.3):
        # Load biến môi trường
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY chưa được thiết lập trong .env")

        # Cấu hình Gemini API
        genai.configure(api_key=api_key)
        self.model_name = model
        self.temperature = temperature
        self.llm = genai.GenerativeModel(model)

        logger.info(f"✅ GeminiManager sẵn sàng (model: {self.model_name}, temp={self.temperature})")

    def generate(self, prompt: str, temperature: float = None) -> str:
        """
        Sinh nội dung từ prompt bằng Gemini.
        """
        temp = temperature if temperature is not None else self.temperature

        logger.debug(f"🔍 Gửi prompt đến Gemini (model={self.model_name}, temp={temp})")
        logger.debug(f"Prompt:\n{prompt}")

        result = self.llm.generate_content(
            prompt,
            generation_config={"temperature": temp}
        )

        logger.info("✅ Sinh nội dung thành công từ Gemini")
        return result.text


if __name__ == "__main__":
    gm = GeminiManager()
    prompt = "Giải thích sự khác nhau giữa list và tuple trong Python."
    output = gm.generate(prompt)
    print("\n=== Gemini Output ===")
    print(output)
