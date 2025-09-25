def pdf_to_json_prompt() -> str:
    return  r"""
    Người dùng sẽ đưa vào 1 file pdf, nhiệm vụ của bạn là chuyển nó về latex.
    Không trả lời hay giải thích gì thêm.
    Lưu ý: Khi gặp link, hãy dùng đúng link thật trong danh sách sau:
        
        {links}
        
    """