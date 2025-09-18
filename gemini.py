from dotenv import load_dotenv
import google.generativeai as genai
import os
from utils import extract_json
from prompt import extract_jd_json_prompt

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY chưa được thiết lập trong .env")

genai.configure(api_key=GOOGLE_API_KEY)
model = "gemini-2.5-flash-lite"
llm = genai.GenerativeModel(model)

def run_gemini(prompt: str, temperature: float = 0.3) -> str:
    result = llm.generate_content(
        prompt,
        generation_config={"temperature": temperature}
    )
    return result.text


