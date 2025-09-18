def extract_jd_json_prompt(jd: str) -> str: 
    return f"""
Bạn là một trình phân tích thông tin tuyển dụng. Hãy đọc nội dung JD dưới đây và trích xuất thông tin, xuất kết quả dưới dạng JSON theo cấu trúc sau:       

{ {
    "Company": [
        { "name": "...", "industry": "...", "size": "...", "country": "..." }
    ],
    "JD": [ { "name": "JD" } ],
    "JobTitle": [ { "name": "..." } ],
    "Skill": [ "..." ],
    "Benefit": [ "..." ],
    "Degree": [ "..." ],
    "Location": [ { "city": "...", "district": "...", "address": "..." } ],
    "Task": [ "..." ]
}  }

    Nguyên tắc trích xuất:

      1. **Company**: Tên công ty, ngành nghề, quy mô, quốc gia nếu có.

      2. **JobTitle**: Chỉ tên vị trí tuyển dụng.

      3. **Skill**: Danh sách tất cả kỹ năng, ngôn ngữ lập trình, framework, tool được nêu trong JD.

      4. **Benefit**: Các phúc lợi, chế độ đãi ngộ, cơ hội thăng tiến, môi trường làm việc.

      5. **Degree**: Các ngành học/ bằng cấp yêu cầu.

      6. **Location**: Trích xuất tất cả địa chỉ làm việc, phân tách thành thành phố, quận/huyện, địa chỉ cụ thể.

      7. **Task**: Trích xuất nhiệm vụ chính của vị trí từ phần mô tả công việc.

      **JD để phân tích:**    

    {jd}      


      **Yêu cầu:**      

    - Chỉ thay đổi giá trị trong các trường JSON dựa trên nội dung JD.

    - Chỉ điền vào những chỗ có dấu 3 chấm.    

    - Phần JobTitle chỉ cần lấy phần tên chính, phần mở ngoặc hay phụ đằng sau thì không cần lấy vào.     

    - Phần Degree chỉ lấy tên chuyên ngành, không cần thêm gì cả (Nếu yêu cầu điểm số hay giải thưởng thì coi như một thực thể luôn) 

    - Kết quả JSON phải hợp lệ, đúng cú pháp.
    
    - Không bỏ sót bất kỳ thông tin nào có trong JD.
"""