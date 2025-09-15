from get_in4 import interactive_cv_optimization_flow

def main():
    jd = """Vị trí: Data Engineer Intern
    Công ty: TechCorp
    Mô tả: Xây dựng và duy trì data pipeline, xử lý big data, tối ưu hóa data warehouse.
    Yêu cầu:
    - Kinh nghiệm dưới 1 năm trong Data Engineering hoặc lĩnh vực liên quan.
    - Thành thạo Python, SQL.
    - Kiến thức về DevOps, CI/CD, cloud (AWS/GCP).
    - Kỹ năng phân tích dữ liệu và machine learning cơ bản.
    - Bằng cử nhân CNTT hoặc tương đương.
    Ưu tiên: Có kinh nghiệm với real-time data processing."""

    cv = """Nguyễn Văn A
    Email: nguyenvana@email.com
    LinkedIn: linkedin.com/in/nguyenvana

    TÓM TẮT
    Software Developer với 2 năm kinh nghiệm phát triển backend, đam mê chuyển sang Data Engineering.

    KINH NGHIỆM
    Software Engineer - Startup XYZ (2022 - hiện tại)
    - Phát triển API backend sử dụng Java Spring Boot.
    - Tích hợp database MySQL, tối ưu query.
    - Làm việc nhóm với Agile/Scrum.

    Junior Developer - Company ABC (2021 - 2022)
    - Xây dựng web app với React và Node.js.
    - Xử lý dữ liệu cơ bản từ API.

    KỸ NĂNG
    - Lập trình: Java, JavaScript, Python, SQL cơ bản.
    - Tools: Git, Docker, Jenkins, Cloud.
    - Cloud: AWS cơ bản (EC2, S3).

    DỰ ÁN
    - E-commerce Backend: Xây dựng REST API cho shop online.
    - Stock Analysis: Sử dụng Machine Learning để phân tích và dự đoán đường đi của cổ phiếu dựa vào mẫu dữ liệu đã được học qua mỗi ngày và sử dụng các kỹ thuật trực quan hóa như matplotlib, seaborn để hiểu rõ pattern của cổ phiếu. 

    HỌC VẤN
    Cử nhân Công nghệ Thông tin - ĐH Bách Khoa Hà Nội (2021)"""

    interactive_cv_optimization_flow(jd, cv, max_gap_questions=2)
if __name__ == "__main__":
    main()