import google.generativeai as genai
from dotenv import load_dotenv
import os

# ====== Load env ======
load_dotenv()


# ====== Cấu hình Gemini ======
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def test_prompt_extract_jd(prompt: str, jd_text: str, model: str = "gemini-2.5-flash"):
    full_prompt = prompt.format(jd_text=jd_text)
    gemini_model = genai.GenerativeModel(model)
    response = gemini_model.generate_content(full_prompt)
    return response.text

if __name__ == "__main__":
    # Prompt theo yêu cầu
    prompt = """
Nhiệm vụ của bạn:
- Tôi sẽ cung cấp một JD (job description) dạng text kèm link ảnh Google Drive.
- Bạn hãy gộp nó thành một dict Python với 2 key:
  - "id_img": chỉ lấy phần ID từ link Google Drive (ví dụ: từ link https://drive.google.com/file/d/1eXp7UbU44Ikj_vwLXZWAd7iy4gZnca7K/view thì id_img = "1eXp7UbU44Ikj_vwLXZWAd7iy4gZnca7K").
  - "content": chứa toàn bộ JD dưới dạng string, giữ nguyên định dạng xuống dòng, không tách nhỏ.

Yêu cầu:
- Không phân tích, không tách field nhỏ.
- Chỉ wrap lại vào dict.
- Nếu JD có xuống dòng thì giữ nguyên y như bản gốc trong value của "content".

Ví dụ output:

{{
  "id_img": "1eXp7UbU44Ikj_vwLXZWAd7iy4gZnca7K",
  "content": \"\"\"<toàn bộ JD giữ nguyên format>\"\"\"
}}

Đây là Job Description cần xử lý:
{jd_text}
"""

    # ====== Thư mục đầu vào và đầu ra ======
    input_dir = "./jd_data"       # thư mục chứa jd1.txt, jd2.txt...
    output_dir = "./jd_out"  # thư mục mới để lưu kết quả

    os.makedirs(output_dir, exist_ok=True)

    # Duyệt qua toàn bộ file txt trong thư mục input
    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]

    for file in files:
        input_path = os.path.join(input_dir, file)
        with open(input_path, "r", encoding="utf-8") as f:
            jd_text = f.read()

        print(f"\n===== Processing {file} =====")
        result = test_prompt_extract_jd(
            prompt=prompt,
            jd_text=jd_text,
            model="gemini-2.5-flash"
        )

        # Tạo file output tương ứng trong thư mục khác
        output_path = os.path.join(output_dir, file.replace(".txt", "_out.txt"))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"--> Saved to {output_path}")

    langfuse.flush()
