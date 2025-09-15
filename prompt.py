from langchain.prompts import ChatPromptTemplate

extract_cv_prompt = ChatPromptTemplate.from_template("""
Bạn là một trợ lý HR. Hãy đọc CV sau và trích xuất thông tin chính: kỹ năng, kinh nghiệm, dự án, học vấn, dưới dạng JSON linh hoạt.
CV: {cv}
Trả lời chỉ JSON.
""")

extract_jd_prompt = ChatPromptTemplate.from_template("""
Trích xuất các yêu cầu chính (kỹ năng, kinh nghiệm, công nghệ/công cụ, trách nhiệm) từ mô tả công việc (JD) sau, dưới dạng JSON.
JD: {jd}
Trả lời chỉ JSON.
""")

optimize_cv_prompt = ChatPromptTemplate.from_template("""
Dựa trên JD: {jd}
Và thông tin CV đầy đủ (bao gồm extra_info từ user): {full_cv_info}

Nhiệm vụ: Tối ưu hóa CV để phù hợp JD.
- Nhấn mạnh match (e.g., backend → data processing).
- Tích hợp extra_info vào kinh nghiệm/dự án/kỹ năng.
- Cấu trúc: Tên, Tóm tắt, Kinh nghiệm, Kỹ năng, Dự án, Học vấn.
- Nếu thiếu skill, dùng transferable (e.g., "backend experience applies to ETL").
Trả lời chỉ JSON với "optimized_cv": text CV.
""")

gap_prompt = ChatPromptTemplate.from_template("""
JD yêu cầu: {jd_requirements}
CV hiện tại có: {cv_info}

Nhiệm vụ:
1.  Phân tích yêu cầu từ JD và thông tin từ CV để tìm ra *gap quan trọng nhất* (yêu cầu cốt lõi của JD chưa được thể hiện rõ hoặc hoàn toàn thiếu trong CV).
2.  Ưu tiên các gap liên quan đến:
    *   **Chức năng/Vai trò cốt lõi**: Liệu CV có kinh nghiệm trực tiếp với loại chức năng/vai trò mà JD yêu cầu không (ví dụ: Marketing Manager cần kinh nghiệm quản lý chiến dịch, không chỉ là kinh nghiệm Sales chung chung).
    *   **Kỹ năng/Công cụ/Phương pháp làm việc chuyên biệt**: Các kỹ năng, công cụ, hoặc phương pháp làm việc được JD nhấn mạnh mà CV không đề cập hoặc đề cập không rõ ràng.
    *   **Dự án/Thành tựu/Sáng kiến liên quan**: Liệu có các dự án, thành tựu, hoặc sáng kiến trong CV thể hiện việc áp dụng các kỹ năng/chức năng JD yêu cầu không.
3.  Dựa trên gap đã xác định, hãy tạo *một câu hỏi rõ ràng, lịch sự và cụ thể* để user cung cấp thêm thông tin.
4.  Câu hỏi nên:
    *   **Nhắc đến yêu cầu cụ thể của JD và điểm chưa rõ trong CV**: Nêu rõ yêu cầu nào từ JD có vẻ thiếu/chưa rõ trong CV của họ.
    *   **Đề xuất loại thông tin cụ thể cần bổ sung**: Gợi ý user nên cung cấp thông tin về dự án, kinh nghiệm thực tế, cách áp dụng kỹ năng, hoặc tình huống cụ thể nào đó.
    *   **Mục đích**: Nhấn mạnh rằng việc này giúp đánh giá rõ hơn sự phù hợp với vị trí.

5.  **Ví dụ về cách xác định gap và đặt câu hỏi:**
    *   **Ví dụ 1 (Ngành IT/Kỹ thuật):**
        *   JD yêu cầu: "Data Engineer: Python, SQL, Data Pipeline, AWS."
        *   CV có: "Software Engineer Java, Spring Boot, Git."
        *   Gap: Thiếu kinh nghiệm về data pipeline, Python/SQL trong ngữ cảnh dữ liệu, và AWS.
        *   Câu hỏi: "Vị trí Kỹ sư Dữ liệu yêu cầu kinh nghiệm chuyên sâu về xây dựng các hệ thống xử lý dữ liệu (Data Pipeline) bằng Python/SQL, và làm việc với các nền tảng đám mây như AWS. Trong CV của bạn, chúng tôi nhận thấy kinh nghiệm chính là Kỹ sư Phần mềm với Java. Bạn có thể chia sẻ thêm về bất kỳ dự án hoặc kinh nghiệm nào bạn đã có liên quan đến việc xử lý dữ liệu, xây dựng pipeline, hoặc sử dụng Python/SQL trong ngữ cảnh dữ liệu, cũng như kinh nghiệm với AWS/GCP không? Điều này sẽ giúp chúng tôi đánh giá mức độ phù hợp của bạn với vai trò Kỹ sư Dữ liệu."
    *   **Ví dụ 2 (Ngành Marketing/Kinh doanh):**
        *   JD yêu cầu: "Trưởng phòng Marketing: Quản lý chiến dịch tích hợp, Phân tích thị trường, Brand Strategy."
        *   CV có: "Chuyên viên Sales 3 năm, có kinh nghiệm chốt sales và xây dựng mối quan hệ khách hàng."
        *   Gap: Thiếu kinh nghiệm quản lý chiến dịch tổng thể, phân tích thị trường, xây dựng chiến lược thương hiệu.
        *   Câu hỏi: "Vị trí Trưởng phòng Marketing yêu cầu khả năng quản lý các chiến dịch tích hợp, phân tích thị trường chuyên sâu và xây dựng chiến lược thương hiệu. Mặc dù bạn có kinh nghiệm xuất sắc trong Sales, bạn có thể chia sẻ về bất kỳ dự án, sáng kiến hoặc tình huống nào bạn đã tham gia vào việc lập kế hoạch, triển khai và đánh giá các chiến dịch marketing tổng thể, hoặc phân tích xu hướng thị trường để định hình chiến lược sản phẩm/dịch vụ không? Thông tin này sẽ giúp chúng tôi đánh giá khả năng lãnh đạo marketing của bạn."
    *   **Ví dụ 3 (Ngành Tài chính/Kế toán):**
        *   JD yêu cầu: "Kế toán Tổng hợp: Lập báo cáo tài chính hợp nhất, Phân tích biến động doanh thu/chi phí, Sử dụng phần mềm SAP."
        *   CV có: "Kế toán viên 2 năm, chịu trách nhiệm ghi sổ, đối chiếu công nợ, kê khai thuế."
        *   Gap: Thiếu kinh nghiệm lập báo cáo hợp nhất, phân tích tài chính sâu, và kinh nghiệm với SAP.
        *   Câu hỏi: "Vị trí Kế toán Tổng hợp của chúng tôi đòi hỏi kinh nghiệm lập báo cáo tài chính hợp nhất, phân tích biến động tài chính chi tiết, và ưu tiên kinh nghiệm với phần mềm SAP. Trong CV của bạn, chúng tôi thấy bạn có kinh nghiệm vững chắc trong vai trò Kế toán viên. Bạn có thể cung cấp thêm thông tin về bất kỳ kinh nghiệm nào bạn đã có trong việc lập các loại báo cáo tài chính phức tạp hơn, tham gia vào các hoạt động phân tích tài chính, hoặc đã từng sử dụng phần mềm kế toán chuyên sâu như SAP hoặc các hệ thống ERP tương tự không? Điều này sẽ giúp chúng tôi có cái nhìn toàn diện hơn về năng lực của bạn."

6.  Nếu không tìm thấy gap quan trọng nào (không cần 100% match hoàn hảo, chỉ cần không có thiếu sót lớn ảnh hưởng đến vai trò cốt lõi), hãy trả lời "DONE".

Trả lời CHỈ dưới dạng JSON: {{"question": "câu hỏi cụ thể hoặc DONE"}}
""")

integrate_extra_info_prompt = ChatPromptTemplate.from_template("""
Dựa trên thông tin CV ban đầu (dạng JSON) và thông tin bổ sung từ user, hãy cập nhật thông tin CV ban đầu để tích hợp các chi tiết mới.
- Thêm các kỹ năng mới vào mục 'kỹ năng'.
- Thêm các dự án mới hoặc chi tiết về dự án vào mục 'kinh nghiệm' hoặc 'dự án'.
- Thêm các kinh nghiệm làm việc cụ thể nếu user mô tả.
- Ưu tiên giữ cấu trúc và phong cách của CV ban đầu nếu có thể, chỉ bổ sung thông tin mới.

Thông tin CV ban đầu: {current_cv_info_json}
Thông tin bổ sung từ user: {user_extra_info}

Trả lời CHỈ JSON của CV đã cập nhật.
""")