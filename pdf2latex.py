import base64
from pathlib import Path
import google.generativeai as genai
from utils import Utils
from prompts.pdf_to_json_prompt import pdf_to_json_prompt
from config.settings import Settings

GEMINI_API_KEY = Settings.GOOGLE_API_KEY
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY chưa được thiết lập trong .env")

genai.configure(api_key=GEMINI_API_KEY)


def pdf_to_latex_with_links(pdf_path: str, model: str = "gemini-2.5-flash-lite") -> str:
    """
    Chuyển PDF thành LaTeX, đảm bảo giữ đúng hyperlink gốc trong file.
    """
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {pdf_path}")

    pdf_base64 = base64.b64encode(pdf_file.read_bytes()).decode("utf-8")

    links = Utils.extract_links_from_pdf(pdf_path)
    
    prompt_text = pdf_to_json_prompt()
    prompt_text = prompt_text.format(links=links)

    model = genai.GenerativeModel(model)

    response = model.generate_content([
        prompt_text,
        {
            "mime_type": "application/pdf",
            "data": pdf_base64,
        }
    ])

    output = response.text
    output_latex = Utils.extract_latex(output)
    with open("data/output.tex", "w", encoding="utf-8") as f:
        f.write(output_latex)
    return output_latex
    
