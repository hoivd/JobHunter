from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import subprocess, os, base64, tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend localhost
    allow_methods=["*"],
    allow_headers=["*"],
)

def build_pdf_from_latex(latex_code: str) -> str:
    """
    Nhận LaTeX string, build PDF, trả về base64 của PDF
    """
    # Tạo file tạm thời .tex
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "document.tex")
        pdf_path = os.path.join(tmpdir, "document.pdf")

        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)

        # Build PDF bằng pdflatex
        cmd = ["pdflatex", "-interaction=nonstopmode", tex_path]
        result = subprocess.run(cmd, cwd=tmpdir, capture_output=True, text=True)

        if result.returncode != 0:
            # Nếu lỗi, trả về thông tin lỗi
            error_msg = f"Error compiling LaTeX:\n{result.stdout}\n{result.stderr}"
            raise Exception(error_msg)

        # Đọc file PDF và encode base64
        with open(pdf_path, "rb") as f:
            pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

    return pdf_base64


@app.post("/compile_latex/")
async def compile_latex(latex: str = Form(...)):
    try:
        pdf_base64 = build_pdf_from_latex(latex)
        return {"success": True, "pdf_base64": pdf_base64}
    except Exception as e:
        return {"success": False, "error": str(e)}
