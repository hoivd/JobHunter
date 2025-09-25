from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import base64

app = FastAPI()

# CORS để frontend React kết nối
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production thì chỉnh domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/compile_latex/")
async def compile_latex(latex: str = Form(...)):
    # Tạo folder tạm
    os.makedirs("tmp", exist_ok=True)
    tex_file = "tmp/temp.tex"
    pdf_file = "tmp/temp.pdf"

    # Ghi LaTeX vào file
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(latex)

    # Biên dịch bằng pdflatex
    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory=tmp", tex_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr.decode()}

    # Đọc PDF và encode base64
    with open(pdf_file, "rb") as f:
        pdf_bytes = f.read()
        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

    return {"pdf_base64": pdf_base64}
