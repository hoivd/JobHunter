from ...state import State

class AgentPlanFindInfo:
    """Agent 3: Lập kế hoạch thu thập thông tin còn thiếu"""
    def __init__(self, llm):
        self.llm = llm

    def __call__(self, state: State):
        prompt = f"""
Bạn là một hệ thống lập kế hoạch thông minh để hỗ trợ thu thập thông tin chuẩn bị viết CV.  
Nhiệm vụ của bạn là xác định **mission to complete** – tức là các nhiệm vụ cụ thể để thu thập đủ thông tin cần thiết trước khi bắt đầu viết CV.  

---

### Quy tắc khi sinh mission
- Mỗi mission phải có:  
  - **name**: tên nhiệm vụ.  
  - **goal**: mục tiêu chính.  
  - **objective**: mô tả chi tiết (càng cụ thể càng tốt), bao gồm:  
    - Yêu cầu số lượng mục tối thiểu.  
    - Yêu cầu mức độ chi tiết.  
    - **Định nghĩa**: giải thích chi tiết thông tin đó là gì và tại sao quan trọng trong CV - giải thích từng yếu tố mẫu thông tin.  
    - **Mẫu cấu trúc**: khung gợi ý để user điền.  
    - **Ví dụ minh họa**: ít nhất 1–2 ví dụ cụ thể đầy đủ cho từng yếu tố.  
    - **Ghi chú bổ sung**: tip để viết ấn tượng, lỗi thường gặp cần tránh.  
    - **Liên hệ trực tiếp với JD**: phải phân tích JD đã cho và chỉ rõ những yêu cầu nào cần được phản ánh trong phần này. Ví dụ:  
      * Nếu JD yêu cầu "kinh nghiệm với Python, PyTorch" → nhấn mạnh trong mission Work Experience hoặc Projects cần bổ sung trải nghiệm đó.  
      * Nếu JD yêu cầu "chứng chỉ AWS" → mission Certifications phải nêu rõ chứng chỉ này.  
      * Nếu JD yêu cầu "kỹ năng quản lý nhóm" → mission Skills phải bao gồm kỹ năng mềm này.  

- **Lưu ý quan trọng**: Phân biệt rõ **Kinh nghiệm làm việc (Work Experience)** và **Dự án (Projects)**.  
  - **Work Experience**: chỉ bao gồm công việc thực tế tại công ty/doanh nghiệp (full-time, part-time, internship).  
  - **Projects**: bao gồm dự án học thuật, cá nhân, nghiên cứu, hoặc cuộc thi.  
  - Phần mục tiêu nghề nghiệp không lên kế hoạch thu thập.  
  - Không tạo phần viết tóm tắt sự nghiệp để cho người dùng tự viết 

- **Điều kiện bỏ qua mission Work Experience**:  
  - Ứng viên là sinh viên/chưa từng đi làm (thông tin trong evaluation/candidate_info xác nhận).  
  - Ứng viên chỉ có dự án học thuật/cá nhân, không có công việc chính thức/thực tập.  
  - JD không yêu cầu bắt buộc kinh nghiệm (ví dụ: tuyển fresher/intern).  
  → Trong các trường hợp này, bỏ qua mission Work Experience và thay bằng mission “Internships/Projects”.  
---

## Đầu vào bạn nhận được:
- candidate_info: {state['cv_info']}  
- evaluation: {state['analysis_result']}  
- job_description: {state['jd_extracted']}  

---

## Định dạng đầu ra (JSON, giữ nguyên khi render, không để .format() thay thế):

{{
  "missions": [
    {{
      "name": "Thu thập Kinh nghiệm làm việc (Work Experience)",
      "goal": "Có đủ thông tin kinh nghiệm tại doanh nghiệp/thực tập",
      "objective": "Yêu cầu: ít nhất 2–3 công ty/vị trí (bao gồm thực tập nếu có). Mỗi vị trí cần: tên công ty, chức danh, thời gian, nhiệm vụ chính, công nghệ sử dụng, thành tựu định lượng.  
Định nghĩa: Work Experience là kinh nghiệm làm việc thực tế tại doanh nghiệp/tổ chức, chứng minh năng lực áp dụng trong môi trường chuyên nghiệp. Không bao gồm dự án học thuật/cá nhân.  
Mẫu cấu trúc: 'Công ty [Tên], Vị trí [Chức danh], [Thời gian] – Nhiệm vụ chính: […]; Công nghệ: […]; Thành tựu: […].'  
Ví dụ: 'FPT Software, Thực tập sinh AI Engineer, 06/2022–09/2022: Tham gia xây dựng hệ thống OCR, áp dụng TensorFlow, giúp cải thiện tốc độ xử lý hóa đơn +25%.'  
Ghi chú: Nếu ứng viên chưa đi làm hoặc JD không yêu cầu kinh nghiệm → bỏ qua mission này và thay bằng 'Internships/Projects'.",
      "priority": "high"
    }},
    {{
      "name": "Thu thập Dự án/Thành tích (Projects/Achievements)",
      "goal": "Bổ sung minh chứng năng lực qua dự án",
      "objective": "Yêu cầu: ít nhất 1–2 dự án nổi bật. Mỗi dự án cần: tên dự án, mô tả ngắn, vai trò, công nghệ sử dụng, kết quả định lượng.  
Định nghĩa: Projects/Achievements là minh chứng cho kỹ năng thông qua dự án học thuật, nghiên cứu, cá nhân hoặc cuộc thi. Dành cho cả sinh viên chưa đi làm.  
Mẫu cấu trúc: 'Dự án [Tên], Vai trò [X], Công nghệ [Y], Kết quả [Z].'  
Ví dụ: 'Dự án Legal Retrieval, Leader: Fine-tune BERT với Hugging Face Transformers, đạt MRR@10 = 0.72, giúp giảm 30% thời gian tìm kiếm tài liệu pháp lý.'  
Ghi chú: Chỉ đưa những dự án có ý nghĩa, liên quan tới JD. Không liệt kê bài tập nhỏ hoặc project lặt vặt.",
      "priority": "medium"
    }}
  ],
  "priority_order": ["missions liên quan JD", "missions khác"]
}}
"""
        print("\n=== Agent Plan Find Info ===")
        result = self.llm.invoke(prompt).content
        print("Output từ LLM:\n", result)
        state["plan_result"] = result
        return {"plan_result": result, "current_step": "agent_plan_find_info"}