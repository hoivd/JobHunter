from langfuse import Langfuse
from langfuse import observe, get_client
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# ====== Cấu hình Langfuse ======
langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@observe
def test_prompt(prompt: str, cv_text: str, model: str = "gemini-1.5-flash"):
    # Tạo prompt hoàn chỉnh
    full_prompt = prompt.format(cv_text=cv_text)

    gemini_model = genai.GenerativeModel(model)
    response = gemini_model.generate_content(full_prompt)
    return response.text
 
if __name__ == "__main__":
    prompt = """
Bạn là một chuyên gia tuyển dụng. 
Nhiệm vụ: Phân tích bộ thông tin mà người dùng cung cấp để kiểm tra xem nó đã đủ thông tin để xây dựng một CV hoàn chỉnh, theo cấu trúc chuẩn hay chưa. 
Lưu ý: Hãy suy nghĩ từng bước.

Một CV chuẩn thường bao gồm tối thiểu:
- Thông tin cá nhân (họ tên, email, số điện thoại, địa chỉ)
- Tóm tắt/Mục tiêu nghề nghiệp
- Kinh nghiệm làm việc (công ty, vị trí, thời gian, mô tả, thành tích)
- Học vấn (trường, chuyên ngành, thời gian học)
- Kỹ năng (kỹ năng cứng, kỹ năng mềm)
- Dự án/Thành tích nổi bật (nếu có)
- Chứng chỉ/Giải thưởng (nếu có)

Đây là bộ thông tin cần đánh giá:
{cv_text}

Hãy trả lời theo định dạng:
1. Đánh giá mức độ đầy đủ (Đủ / Thiếu).
2. Các phần còn thiếu hoặc chưa rõ ràng.
3. Gợi ý cụ thể những gì cần bổ sung để hoàn thiện CV
    """
    cv_text = """
    Early-career AI/ML engineer with hands-on experience in Deep Learning, NLP, and transformer-based models. Built end-to-end systems in academic projects and hackathons, including LLM integration, semantic search, and real-time data pipelines. Strong Python skills (OOP, design patterns) and proven ability to collaborate in team projects. Eager to apply technical expertise to production systems and grow as an AI Engineer. Technical Skills • Machine Learning Frameworks: PyTorch, Tensorflow, Pandas, Scikit-learn, Matplotlib. • Big Data Tools: Apache Hadoop, Apache Spark, Apache Kafka. • Programming Languages: Python, C++. • Database: MySQL, MongoDB. • Other Tools: Git, Docker, Selenium, Jupyter.

"""
    result = test_prompt(
        prompt,
        cv_text,
        "gemini-2.5-flash-lite"
    )
    print(result)
    langfuse.flush()