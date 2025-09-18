from utils import extract_json, generate_cypher_from_json
from gemini import run_gemini
from prompt import extract_jd_json_prompt
import json
from queries import push_cypher_code
from db import close_driver

def main(jd: str):
    prompt = extract_jd_json_prompt(jd)
    json_jd = run_gemini(prompt, temperature=0.3)
    json_jd = extract_json(json_jd)
    json_jd = json.loads(json_jd)
    cypher_jd = generate_cypher_from_json(json_jd, out_path="output.cypher")
    push_cypher_code(cypher_jd)
    
    close_driver()

if __name__ == "__main__":
    jd = f"""AI Architect (Python, Microservices, Docker)
    ABBANK
    Sign in to view salary

    36 Hoàng Cầu, Dong Da, Ha Noi  At office 11 days ago
    Skills:
    Job Expertise:
    Job Domain:
    Top 3 reasons to join us
    Lương/ thưởng hấp dẫn
    Cơ hội thăng tiến nghề nghiệp cao
    Môi trường làm việc thân thiện, năng động
    Job description
    1. Trách nhiệm trong Xây dựng và quản lý thiết kế nền tảng AI:
    Thiết kế và xây dựng nền tảng AI nhằm phát triển các ứng dụng AI với các agentic AI và tinh chỉnh các mô hình sử dụng LLM, VLM.
    Dẫn dắt nhóm phát triển AI thực hiện dự án bằng cách cung cấp hướng dẫn kỹ thuật trong suốt vòng đời phát triển phần mềm.
    Xác định chiến lược AI và hợp tác chặt chẽ với các bên liên quan trong doanh nghiệp để đảm bảo các giải pháp AI phù hợp với mục tiêu của tổ chức.
    Thiết kế và tối ưu hóa các mô hình AI để đảm bảo khả năng mở rộng, hiệu suất và hiệu quả.
    Cung cấp sự lãnh đạo và cố vấn kỹ thuật cho các kỹ sư AI, thúc đẩy văn hóa đổi mới và cải tiến liên tục.
    Tiến hành nghiên cứu và phát triển chuyên sâu để khám phá các công nghệ và phương pháp luận AI mới.
    Giám sát việc tích hợp các giải pháp AI với các hệ thống và quy trình kinh doanh hiện có, đảm bảo việc triển khai và vận hành suôn sẻ.
    Phối hợp với ban lãnh đạo để xác định tầm nhìn và lộ trình AI cho tổ chức
    2. Thúc đẩy và lan tỏa việc sử dụng AI tới ABBankers và đội ngũ công nghệ:
    Định kỳ tổ chức các buổi truyền thông về AI và cách sử dụng các ứng dụng AI trên thị trường, và các ứng dụng AI do ABBANK phát triển để giúp người dùng nâng cao nhận thức về AI, nâng cao năng suất, hiệu quả trong công việc.
    Thu thập các usecase từ người dùng nghiệp vụ ABBANK để đưa vào danh sách phát triển.
    Thường xuyên tổ chức hoặc dẫn dắt tổ chức các buổi giới thiệu về sản phẩm AI, công nghệ AI, đề xuất ứng dụng AI, ... tới đội ngũ công nghệ nhằm lan tỏa và thúc đẩy việc ứng dụng AI và tích hợp AI vào các giải pháp công nghệ
    3. Xây dựng kế hoạch ngân sách và quản lý ngân sách bộ phận:
    Phối Lập ngân sách cho hoạt động của Đơn vị một cách chính xác và hiệu quả.
    Your skills and experience
    Bằng cấp: Tốt nghiệp Đại học trở lên các chuyên ngành Công nghệ thông tin/ Điện tử viễn thông/ Toán tin.
    Kinh nghiệm:
    Có từ 5 năm kinh nghiệm trở lên trong lĩnh vực AI; đã tham gia trực tiếp xây dựng và dẫn dắt xây dựng các ứng dụng AI
    Kỹ năng kỹ thuật:
    Thành thạo ngôn ngữ Python
    Có kinh nghiệm toàn diện với LangChain API, LLamaIndex và các công nghệ cơ sở dữ liệu (MongoDB, PostgreSQL, ChromaDB, VespaDB, v.v.).
    Có kinh nghiệm sâu rộng với microservices, Docker và tối ưu hóa, mở rộng microservices.
    Why you'll love working here
    Lương và phúc lợi hấp dẫn:
    Mức lương cạnh tranh, phản ánh trực tiếp kỹ năng và kinh nghiệm của ứng viên (chi tiết sẽ được thảo luận trong buổi phỏng vấn)
    13 ngày nghỉ phép linh hoạt, bao gồm ngày sinh nhật và các dịp quan trọng khác
    Bảo hiểm đầy đủ theo luật lao động, cùng với ABBANK CARE - chương trình phúc lợi bổ sung đặc biệt dành cho ABBankers
    Lãi suất vay ưu đãi - Quyền lợi đặc biệt dành cho nhân viên ABBANK
    Cơ hội phát triển nghề nghiệp hấp dẫn:
    Gia nhập các dự án chuyển đổi quy mô lớn, cộng tác cùng các chuyên gia hàng đầu để áp dụng công nghệ mới nhất trong ngành ngân hàng
    Lộ trình phát triển sự nghiệp rõ ràng, được tạo điều kiện cho cả sự phát triển kỹ thuật và quản lý
    Hỗ trợ đào tạo và chứng chỉ trong lĩnh vực IT, ngân hàng/tài chính
    Môi trường làm việc năng động:
    Mô hình làm việc linh hoạt, trẻ trung, khuyến khích đổi mới và sáng tạo
    Văn phòng được trang bị hiện đại, kèm theo các thiết bị tiên tiến nhất dành cho nhân viên
    Tổ chức thường xuyên các hoạt động ngoại khóa (team building, hội thảo, và các sự kiện văn nghệ), tạo điều kiện cho nhân viên gắn kết và phát triển

    ABBANK
    Cung ứng các sản phẩm - dịch vụ tài chính ngân hàng trọn gói
    Company typeCompany industryCompany size
    Non-IT
    Banking
    1000+
    CountryWorking daysOvertime policy
    VietnamMonday - FridayNo OT
    """

    main(jd)
    
