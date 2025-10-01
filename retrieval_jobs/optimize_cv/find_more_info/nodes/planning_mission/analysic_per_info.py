from ...state import State

class AgentAnalysisPerInfo:
    """Agent 2: Phân tích CV hiện tại so với JD"""
    def __init__(self, llm):
        self.llm = llm

    def __call__(self, state: State):
        prompt = f"""
Bạn là một chuyên gia tuyển dụng.  
Nhiệm vụ: Phân tích bộ thông tin mà người dùng cung cấp để kiểm tra xem nó đã đủ thông tin để xây dựng một CV hoàn chỉnh theo **các mục chuẩn** hay chưa.  

### Hướng dẫn:
- Hãy suy nghĩ từng bước (theo Chain of Thought).  
- So sánh bộ thông tin {state['cv_info']} với **các mục chuẩn trong một CV hoàn chỉnh**.  

### Checklist CV chuẩn cho ứng viên có kinh nghiệm:
1. Header (Thông tin cá nhân: họ tên, email, số điện thoại, địa chỉ, link LinkedIn/GitHub nếu có).  
2. Career Summary / Mục tiêu nghề nghiệp.  
3. Education (tối thiểu 1 bậc học: trường, chuyên ngành, thời gian học, thành tích nếu có).  
4. Skills (3–5 kỹ năng cứng, 2–3 kỹ năng mềm).  
5. Projects / Key Achievements (ít nhất 3-5 dự án nổi bật; mô tả ngắn gọn gồm vai trò, công nghệ, kết quả, tác động).  
6. Certifications / Honors & Awards (1–2 mục, nếu có).  
7. Additional Information (ngôn ngữ, sở thích, hoạt động khác nếu có).  

### Checklist CV cho sinh viên/chưa có kinh nghiệm:
1. Header (Thông tin cá nhân).  
2. Career Summary / Objective (mục tiêu nghề nghiệp, lĩnh vực mong muốn).  
3. Education (trường, chuyên ngành, GPA/thành tích học tập, học bổng nếu có).  
4. Projects / Internships (2–3 dự án hoặc kỳ thực tập; mô tả gồm vai trò, công nghệ, kết quả).  
5. Skills (3–5 kỹ năng cứng, 2–3 kỹ năng mềm).  
6. Competitions / Extracurriculars (Hackathon, CLB, hoạt động tình nguyện).  
7. Certifications (1–2 chứng chỉ online hoặc chuyên ngành).  
8. Additional Information (ngoại ngữ, sở thích, thông tin bổ sung khác).  

- Xác định phần nào đã có, phần nào còn thiếu hoặc chưa rõ ràng.  
- Với mỗi phần thiếu hoặc chưa rõ ràng, đưa ra **hướng dẫn thu thập thông tin cụ thể**, bao gồm:  
  - Thông tin cần bổ sung.  
  - Số lượng tối thiểu khuyến nghị.  
  - Mức độ chi tiết mong đợi.  
  - **Định nghĩa**: giải thích khái niệm và tại sao quan trọng.  
  - **Ví dụ minh họa**: 1–2 mẫu nội dung cụ thể để user dễ hình dung, phải ví dụ cho từng thông tin cần bổ sung 
1
### Định dạng bắt buộc để trả lời:
1. Đánh giá mức độ đầy đủ (Đủ / Thiếu).  
2. Các mục còn thiếu hoặc chưa rõ ràng.  
3. Hướng dẫn chi tiết bổ sung cho từng mục:  
   - Thông tin cần thu thập.  
   - Số lượng mục tối thiểu.  
   - Mức độ chi tiết yêu cầu.  
   - Định nghĩa: Phải định nghĩa cho từng yếu tố thông tin của mục cần bổ sung luôn
   - Ví dụ minh họa: 1–2 mẫu nội dung cụ thể để user dễ hình dung, phải ví dụ cho từng thông tin cần bổ sung 

 
"""
        print("\n=== Agent Analysis Per Info ===")
        result = self.llm.invoke(prompt).content
        print("Output từ LLM:\n", result)
        state["analysis_result"] = result
        return {"analysis_result": result, "current_step": "agent_analysis_per_info"}