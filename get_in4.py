import json
from llm_utils import (
    extract_requirements,
    extract_cv_info,
    generate_gap_question,
    integrate_extra_info,
    optimize_cv_final
)

def interactive_cv_optimization_flow(jd_text: str, cv_text: str, max_gap_questions: int = 2):
    print("--- BẮT ĐẦU QUY TRÌNH TỐI ƯU CV ---")

    # 1. Trích xuất yêu cầu JD
    print("1. Trích xuất yêu cầu từ JD...")
    jd_requirements = extract_requirements(jd_text)
    print(f"   JD yêu cầu: {json.dumps(jd_requirements, indent=2, ensure_ascii=False)}\n")

    # 2. Trích xuất thông tin CV ban đầu
    print("2. Trích xuất thông tin từ CV ban đầu...")
    full_cv_info = extract_cv_info(cv_text)
    print(f"   Thông tin CV: {json.dumps(full_cv_info, indent=2, ensure_ascii=False)}\n")

    gap_rounds = 0
    while gap_rounds < max_gap_questions:
        print(f"3. Lần hỏi thông tin bổ sung thứ {gap_rounds + 1}...")
        
        current_gap_question = generate_gap_question(jd_requirements, full_cv_info)
        
        if current_gap_question == "DONE":
            print("   Chatbot: Không có gap quan trọng nào. Tiến hành tối ưu CV.")
            break
        
        print(f"   Chatbot: {current_gap_question}")
        user_response = input("   Bạn (nhập thông tin bổ sung, hoặc 'Không có' để dừng): ").strip()
        
        if not user_response or user_response.lower() in ["không có", "khong co", "stop", "dừng"]:
            print("   Chatbot: Tiếp tục tối ưu CV với thông tin hiện có.")
            break
            
        print("   Chatbot: Đang tích hợp thông tin bổ sung vào CV...")
        full_cv_info = integrate_extra_info(full_cv_info, user_response)
        print("   Chatbot: Đã cập nhật thông tin CV.")
        
        gap_rounds += 1
        
    if gap_rounds == max_gap_questions:
        print(f"\n   Chatbot: Đã đạt giới hạn {max_gap_questions} lần hỏi. Tiếp tục tối ưu CV.")

    # 4. Tối ưu hóa CV cuối cùng
    print("\n4. Tiến hành tối ưu hóa CV để phù hợp với JD...")
    optimized_cv = optimize_cv_final(jd_text, full_cv_info)
    print("--- CV ĐÃ TỐI ƯU ---")
    print(optimized_cv)
    print("--------------------")

    return optimized_cv
