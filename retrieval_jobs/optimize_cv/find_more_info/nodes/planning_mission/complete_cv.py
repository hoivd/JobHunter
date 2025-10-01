from ...state import State

class AgentCompleteCV:
    """Agent 3: Hoàn thiện CV dựa trên thông tin đã có"""
    def __init__(self, llm):
        self.llm = llm

    def __call__(self, state: State):
        print("\n=== Agent Complete CV ===")
        collected_info = state.get("mission_final_state", {}).get("collected_info", [])
        cv_info = state.get("cv_info", "")
        analysis = state.get("analysis_result", "")

        prompt = f"""
Bạn là một chuyên gia viết CV chuyên nghiệp.  
Nhiệm vụ: Dựa trên thông tin người dùng cung cấp ({cv_info}),({collected_info}) và kết quả phân tích thiếu sót ({analysis}), hãy viết thành một bản CV hoàn chỉnh, theo bố cục chuẩn quốc tế, bằng tiếng Anh.

### Yêu cầu định dạng:
- CV phải rõ ràng, súc tích, chuyên nghiệp, ATS-friendly.  
- Trình bày theo các mục chuẩn:  
  1. Header (Full name, contact info, LinkedIn/GitHub).  
  2. Career Summary / Objective (2–3 câu).  
  3. Education (University, major, GPA, time).  
  4. Skills (Technical + Soft skills).  
  5. Projects / Achievements (ít nhất 2 dự án, mỗi dự án có: tên, vai trò, mô tả ngắn, công nghệ, kết quả/impact).  
  6. Certifications / Awards (nếu có).  
  7. Languages (nếu có).  
  8. Optional: Extracurriculars/Interests nếu có dữ liệu.  

- Nội dung phải dùng ngôn ngữ hành động (action verbs: Led, Designed, Implemented...).  
- Mỗi dự án/achievement trình bày dạng bullet points.  
- Career Summary phải thể hiện định hướng nghề nghiệp, giá trị và điểm mạnh.  

### Output format:
Viết CV hoàn chỉnh dưới dạng ngôn ngữ latex.
"""
        print(prompt)

        print("\n=== Agent Complete CV ===")
        result = self.llm.invoke(prompt).content
        print("Output từ LLM:\n", result)

        state["completed_cv"] = result
        return {"completed_cv": result, "current_step": "agent_complete_cv"}
    


# ===================== TEST MAIN =====================
if __name__ == "__main__":
    # ⚡ nhập API key thật vào đây
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    # Khởi tạo LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0,
        api_key=api_key,
    )

    # Giả lập dữ liệu CV
    cv_info = ['{"full_name": "Đặng Vĩnh Hội", "phone_number": "0969.501.261", "email": "hoivd79@gmail.com", "address": "Gò Vấp, Thành phố Hồ Chí Minh", "linkedin": "hoivd", "github": "hoivd"}', '{"education": {"university": "Trường Công nghệ thông tin UIT", "major": "Khoa học Máy tính", "time": "2022 - 2026", "gpa": "3.1/4", "achievements": "Không có thành tích nổi bật"}}', '{"Career Summary/Objective": "Bỏ qua"}', '{"projects_achievements": [{"project_name": "CRIMEScan: AI System for Automated Web Collection and Risk Alert For Bankings System", "role": "Team Lead", "description": "An end-to-end modular system that automates the collection, classification, and analysis of crime-related articles. It combines a crawler, information extraction, cross-identification, and a dashboard to build a searchable criminal database and handle customer queries.", "technologies_used": "Python, Bedrock LLM, Cohere Embeddings, Faiss (Vector Databases)", "results_impact": "Customized the Crawl4AI tool with Bedrock LLM to enable automated crawling and classification of crime-related articles, significantly reducing processing time. Developed a criminal information extraction module by designing Named Entity Recognition (NER) prompts, achieving 95% accuracy. Built a Cross-Identification algorithm with 98.7% accuracy for constructing a criminal database and enabling customer queries, leveraging semantic search with Faiss and Cohere Embeddings. Implemented logging utilities to monitor pipeline execution and detect anomalies in real time. Designed and integrated a dashboard for seamless querying and analysis of criminal data."}, {"project_name": "Legal Document Retrieval", "role": "AI Engineer", "description": "A legal document retrieval system designed to handle text-based queries effectively by combining retrieval and ranking models.", "technologies_used": "Transformer-based Models, Pytorch, Hugging Face Transformers", "results_impact": "Top 3 SOCIT Competition, Accuracy: 0.71"}]}]', '{"Kỹ năng cứng": "Lập trình Python (thiết kế hướng đối tượng, design patterns), Large Language Models (LLMs), multi-agent frameworks, semantic search, transformer models", "Kỹ năng mềm": "Giải quyết vấn đề tốt"}', '{"Certifications/Honors & Awards": [{"certificate_name": "top 3 SOCIT", "issuer": "Đại học HUST", "date": "2024"}, {"certificate_name": "Chung kết VPBank Hackathon", "issuer": "VPBank", "date": "2025"}]}', '{"language": "Tiếng Anh (đọc tài liệu tiếng Anh)"}']
    jd_extracted  = """
**1. Chức danh công việc:**
Software Engineering Internship – AI Systems Development - Fall 2025

**2. Mô tả công việc (nhiệm vụ chính):**
*   Phát triển và triển khai các mô hình học máy tiên tiến để phát hiện các mẫu giả mạo định vị (location spoofing) trong các tập dữ liệu lớn.
*   Đóng góp vào việc cải thiện hệ thống AI đa tác tử (multi-agent AI system) được thiết kế để phát hiện gian lận trên các luồng dữ liệu phức tạp.
*   Phát triển và tinh chỉnh các tác tử AI để cải thiện khả năng suy luận, xác thực và ra quyết định.
*   Mở rộng chức năng nền tảng để xử lý các định dạng dữ liệu đa dạng và tích hợp các nguồn dữ liệu mới.
*   Xây dựng các công cụ và tiện ích để hỗ trợ phân tích, kiểm thử và xác minh tự động.
*   Hợp tác với các kỹ sư và nhà nghiên cứu để thiết kế, triển khai và kiểm thử các cải tiến hệ thống.

**3. Yêu cầu bắt buộc (kỹ năng, kinh nghiệm, học vấn):**
*   **Học vấn:** Đang theo học hoặc vừa tốt nghiệp các ngành Khoa học Máy tính, Thống kê, Toán học hoặc các lĩnh vực định lượng liên quan.
*   **Kỹ năng lập trình:** Kỹ năng lập trình Python vững chắc, có kinh nghiệm về thiết kế hướng đối tượng (object-oriented design).
*   **Kiến thức/Kinh nghiệm:**
    *   Có kiến thức hoặc sự quan tâm đến các khái niệm AI/ML, đặc biệt là các mô hình ngôn ngữ lớn (LLMs) và mô hình transformer.
    *   Kỹ năng giải quyết vấn đề tốt và khả năng giải quyết các thách thức kỹ thuật phức tạp.
    *   Sự nhiệt tình trong việc học hỏi công nghệ mới và áp dụng chúng vào các dự án thực tế.

**4. Kỹ năng/kinh nghiệm ưu tiên (nếu có):**
*   Kinh nghiệm khóa học hoặc dự án trong lĩnh vực AI, ML hoặc hệ thống dữ liệu.
*   Kiến thức về các công nghệ chính: Large Language Models, multi-agent frameworks, semantic search, transformer models, Advanced Python development (object-oriented design, design patterns), XML/JSON parsing, embeddings, structured/unstructured data handling, Multi-agent systems, modular design, configuration management.

**5. Quyền lợi / phúc lợi:**
*   Cơ hội làm việc trong một công ty công nghệ "Unicorn" hàng đầu về định vị địa lý, an ninh mạng và chống gian lận.
*   Được tham gia phát triển các công nghệ tiên tiến.
*   Cơ hội học hỏi và phát triển nghề nghiệp liên tục (bao gồm ngân sách phát triển chuyên môn, cơ hội đào tạo, chia sẻ kiến thức).
*   Môi trường làm việc đề cao sự tôn trọng lẫn nhau, hòa nhập và đa dạng.
*   Được đóng góp vào các sáng kiến trách nhiệm xã hội và cộng đồng.
*   Chế độ lương thưởng cạnh tranh, các khoản thưởng và chương trình phúc lợi toàn diện (thông tin chi tiết có thể xem tại: https://www.geocomply.com/careers/internship/).
*   Văn hóa làm việc năng động, có tính tương tác cao.

**6. Địa điểm / Hình thức làm việc:**
*   **Địa điểm:** Văn phòng Thành phố Hồ Chí Minh.
*   **Hình thức làm việc:** Thực tập toàn thời gian (40 giờ/tuần).
*   **Thời gian thực tập:** Tháng 9 - Tháng 12 (4 tháng).
*   **Mô hình làm việc:** Hybrid (kết hợp làm việc tại văn phòng và từ xa, với chính sách 3 ngày làm việc tại văn phòng).
"""

    # Tạo state object giả
    state = State()
    state["cv_info"] = cv_info
    state["jd_extracted"] = jd_extracted
    # Gọi Agent
    agent = AgentCompleteCV(llm)
    output = agent(state)

    print("\n=== Final Completed CV ===")
    print(output["completed_cv"])