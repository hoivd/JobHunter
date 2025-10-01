from langchain.schema import HumanMessage
import json
import re

class GenerateSlotNode:
    def __init__(self, llm):
        """
        - llm: LLM model (vd: ChatGoogleGenerativeAI)
        """
        self.llm = llm

    def __call__(self, state):
        print('\n=== GenerateSlotNode ===')
        mission = state["current_mission"]
        goal = mission.get("goal", "")
        objective = mission.get("objective", "")

        print(f"\n=== Generate slots for mission: {mission.get('name','Unnamed')} ===")
        print(f"🎯 Goal: {goal}")
        print(f"🎯 Objective: {objective}")

        # Prompt cho LLM: sinh ra danh sách slot cần thu thập
        prompt = f"""
Mission: {mission.get("name","")}
Goal: {goal}
Objective: {objective}

Hãy tạo cấu trúc JSON `required_slots` để thu thập thông tin cho mission này.

Yêu cầu:
1. Nếu mission yêu cầu **nhiều mục** (ví dụ: 2–3 dự án, nhiều chứng chỉ, nhiều giải thưởng, nhiều khóa học...), 
   thì trả về một JSON list gồm nhiều object. 
   - Mỗi object đại diện cho một mục. 
   - Các object phải có cùng cấu trúc slot (snake_case, ngắn gọn).
   - Không điền dữ liệu, chỉ để rỗng ("").
2. Nếu mission chỉ yêu cầu **1 mục** → trả về một JSON object chứa các slot cần thu thập.
3. Nếu mission chỉ cần **các field đơn lẻ** (ví dụ: thông tin cá nhân), trả về một JSON list các field (string).
4. Đầu ra chỉ là JSON, không thêm mô tả ngoài.

Ví dụ:
- Mission cần 3 dự án lớn:
[
  {{ "project_name": "", "company": "", "role": "", "timeline": "", "tasks": "", "achievements": "", "technologies": "" }},
  {{ "project_name": "", "company": "", "role": "", "timeline": "", "tasks": "", "achievements": "", "technologies": "" }},
  {{ "project_name": "", "company": "", "role": "", "timeline": "", "tasks": "", "achievements": "", "technologies": "" }}
]

- Mission thu thập chứng chỉ:
[
  {{ "certificate_name": "", "issuer": "", "date": "", "credential_id": "" }},
  {{ "certificate_name": "", "issuer": "", "date": "", "credential_id": "" }}
]

- Mission thu thập thông tin cá nhân:
["full_name", "phone_number", "email", "address", "linkedin", "github"]
"""

     

        # Gọi LLM
        response = self.llm.invoke([HumanMessage(content=prompt)]).content.strip()
        print(f"\n📤 LLM Output (raw):\n{response}")

        # Regex để lấy phần JSON trong code block nếu có
        pattern = r"```json\s*(.*?)\s*```"
        match = re.search(pattern, response, re.DOTALL)

        if match:
            json_str = match.group(1).strip()
        else:
            json_str = response.strip()

        # Parse JSON, fallback nếu lỗi
        try:
            required_slots = json.loads(json_str)
            assert isinstance(required_slots, list)
        except Exception as e:
            print(f"⚠️ Parse JSON thất bại ({e}), fallback về list mặc định")
            required_slots = ["title_or_name", "role_or_position", "timeline", "achievements"]

        # Update mission
        mission["required_slots"] = required_slots

        update = {
            "current_mission": mission,
            "current_step": "generate_slot"
        }
        return update
    
if __name__ == "__main__":
    from langchain_google_genai import ChatGoogleGenerativeAI
    from dotenv import load_dotenv
    import os
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0,
        api_key=api_key,
    )

    # State ban đầu (ví dụ mission cá nhân)
    state = {
        "current_mission":  {
      "name": "Thu thập Kinh nghiệm làm việc/Dự án lớn",
      "goal": "Minh chứng kinh nghiệm thực tế, đặc biệt là các dự án AI/ML, phù hợp với yêu cầu của JD.",
      "objective": "Cần ít nhất 2–3 mục kinh nghiệm/dự án lớn. Mỗi mục cần: tên công ty/tổ chức (hoặc tên dự án), chức danh/vai trò, thời gian thực hiện, mô tả chi tiết nhiệm vụ và trách nhiệm (tập trung vào AI/ML, LLMs, transformer, xử lý dữ liệu, phát triển hệ thống), thành tích đạt được (định lượng hóa nếu có), và các công nghệ/công cụ đã sử dụng (đặc biệt là các công nghệ ưu tiên trong JD: LLMs, transformer models, semantic search, multi-agent systems, Python OOP).",
      "priority": "high"
    }
    }

    # Gọi node generate slot
    slot_node = GenerateSlotNode(llm=llm)
    result = slot_node(state)

    print("\n✅ Kết quả sau GenerateSlotNode:")
    print(json.dumps(result, ensure_ascii=False, indent=2))