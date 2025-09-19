import re
from typing import Optional
import json
from pathlib import Path
from pypdf import PdfReader

def extract_json(text: str) -> Optional[str]:
    pattern = r"```json\s*(\{.*?\})\s*```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else None

def extract_latex(text: str) -> Optional[str]:
    pattern = r"```latex\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else None

def extract_links_from_pdf(pdf_path: str):
    """
    Trích xuất hyperlink thật từ PDF.
    Trả về danh sách {page, uri}.
    """
    reader = PdfReader(pdf_path)
    links = []

    for page_num, page in enumerate(reader.pages, start=1):
        if "/Annots" in page:
            for annot in page["/Annots"]:
                annot_obj = annot.get_object()
                if "/A" in annot_obj and "/URI" in annot_obj["/A"]:
                    links.append({
                        "page": page_num,
                        "uri": annot_obj["/A"]["/URI"]
                    })
    return links