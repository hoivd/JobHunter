from openai import OpenAI
import base64
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def pdf_to_latex(pdf_path: str, model: str = "o4-mini") -> str:
    """
    Chuyển 1 file PDF thành mã LaTeX bằng OpenAI Responses API.
    
    Parameters
    ----------
    pdf_path : str
        Đường dẫn tới file PDF cần chuyển đổi
    model : str
        Tên model OpenAI (mặc định: "o4-mini")
        
    Returns
    -------
    str
        Nội dung LaTeX trả về từ API
    """

    # Đọc pdf và encode base64
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {pdf_path}")
    pdf_base64 = base64.b64encode(pdf_file.read_bytes()).decode("utf-8")

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "developer",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Người dùng sẽ đưa vào 1 file pdf, nhiệm vụ của bạn là "
                            "chuyển nó về latex.\nKhông trả lời hay giải thích gì thêm."
                        )
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "filename": pdf_file.name,
                        "file_data": f"data:application/pdf;base64,{pdf_base64}"
                    }
                ]
            }
        ]
    )

    return response.output_text

# test
output = pdf_to_latex("LeVanHoang_AI_Enginner.pdf")

# lưu output vào file latex.tex
with open("output.tex", "w") as f:
    f.write(output)
