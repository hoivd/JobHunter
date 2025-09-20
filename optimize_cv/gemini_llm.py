from dotenv import load_dotenv
import google.generativeai as genai
import os
from utils import Utils
from logger import _setup_logger

# Load config và logger
config = Utils.get_config()
logger = _setup_logger(__name__, level=config["logging"]["level"])


class GeminiLLM:
    def __init__(self, model: str = "gemini-2.5-flash-lite", temperature: float = 0.3):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY chưa được thiết lập trong .env")

        genai.configure(api_key=api_key)
        self.model_name = model
        self.temperature = temperature
        self.llm = genai.GenerativeModel(model)

        logger.info(f"✅ GeminiManager sẵn sàng (model: {self.model_name}, temp={self.temperature})")

    def generate(self, prompt: str, temperature: float = None) -> str:
        temp = temperature if temperature is not None else self.temperature

        result = self.llm.generate_content(
            prompt,
            generation_config={"temperature": temp}
        )
        return result.text

    def generate_from_pdf(self, pdf_path: str, prompt: str, temperature: float = None) -> str:
        """
        Sinh nội dung từ PDF + prompt bằng Gemini.
        """
        temp = temperature if temperature is not None else self.temperature

        # Upload PDF
        pdf_file = genai.upload_file(pdf_path)

        logger.info(f"📄 Đã upload PDF: {pdf_file.uri}")

        # Multi-modal input: [file, prompt text]
        result = self.llm.generate_content(
            [pdf_file, prompt],
            generation_config={"temperature": temp}
        )

        return result.text


if __name__ == "__main__":
    from prompt_manager import PromptManager
    gm = GeminiLLM()
    pm = PromptManager()

    prompt = pm.load('cv_extractor')
    logger.info(f"prompt: {prompt}")
    # # Ví dụ dùng text
    # prompt = "Giải thích sự khác nhau giữa list và tuple trong Python."
    # print("=== Text Output ===")
    # print(gm.generate(prompt))

    # Ví dụ dùng PDF
    pdf_path = "data/cv_pdhh.pdf"  # đổi thành đường dẫn PDF của bạn
    pdf_prompt = "Tóm tắt nội dung chính của file PDF này."
    print("\n=== PDF Output ===")
    print(gm.generate_from_pdf(pdf_path, prompt))
