from langchain.schema import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.schema import HumanMessage
import json
from ...tools.git_tools import GitHubToolsManager

class PlanningNode:
    def __init__(self, llm, tool_registry):
        """
        - llm: LLM model
        - tool_registry: instance của ToolManagerRegistry (có get_all_tools_text, get_all_tools)
        """
        self.llm = llm  
        self.tool_registry = tool_registry

    def __call__(self, state):
        mission = state["current_mission"]
        print(json.dumps(state, ensure_ascii=False, indent=2))

        history = state.get("history", [])
        goal = mission.get("goal", "")
        objective = mission.get("objective", "")
        required_slots = mission.get("required_slots", [])

        print(f"\n=== Planning for mission: {mission.get('name', 'Unnamed')} ===")
        print(f"🎯 Goal: {goal}")
        print(f"🎯 Objective: {objective}")

        # Format lại history để nhắc LLM
        history_text = "\n".join(
            f"Thought: {h['thought']}\nAction: {h['action']}\nObservation: {h['observation']}"
            for h in history
        ) or "(chưa có lịch sử, bắt đầu mới)"

        # 🔑 Lấy danh sách tools từ registry
        tools_text = self.tool_registry.get_all_tools_text()

        # Prompt cho LLM
        prompt =f"""
Bạn là một Trợ lý AI chuyên sâu trong việc phân tích, chỉnh sửa và viết CV phù hợp với Job Description (JD).
Mục tiêu: **thu thập và tổng hợp tiện lợi nhất đúng—đủ—đáng tin** mọi dữ liệu cần cho CV, đồng thời **giảm thiểu số lần yêu cầu người dùng nhập** (chỉ hỏi khi thật sự cần).

## Mission hiện tại
- Name: {mission.get("name","")}
- Goal: {goal}
- Objective: {objective}
- Required slots: {required_slots}

## Lịch sử trước đó (câu trả lời của người dùng)
{history_text}

## Công cụ có thể dùng (Action)
{tools_text}

---

#### Yêu cầu bắt buộc:
### Bước 0. Slot (hoặc Sub-slot) Tracking theo Objective  
Nhiệm vụ: Với mỗi **slot trong `required_slots` hoặc sub-slot của nó**, hãy phân tích toàn bộ **Action – Observation pairs** có liên quan và xác định trạng thái cuối cùng theo objective.

1. Thu thập tập Action – Observation pairs  
   - Duyệt toàn bộ history.  
   - Với mỗi Observation, ghi kèm Action gốc đã dẫn đến nó.  
   - Gom thành một “tập quan sát” (Observation Set) cho slot/sub-slot.  

2. Đánh giá mức độ liên quan (Relevance Check)  
   - Nếu Action trực tiếp hỏi về slot/sub-slot → Observation liên quan chắc chắn.  
   - Nếu Action gián tiếp (ví dụ hỏi mở) → đánh giá mức độ khớp ngữ nghĩa với slot/sub-slot.  
   - Nếu Action không liên quan → Observation được coi là không liên quan.  

3. Phân tích quan hệ giữa các observation (trong tập)  
   - Bổ sung (Complementary): observation sau cung cấp thêm chi tiết cho observation trước.  
   - Trùng lặp (Redundant): observation lặp lại cùng nội dung → ưu tiên cái rõ ràng, đầy đủ hơn.  
   - Mâu thuẫn (Contradictory): observation khác nhau/đối lập → cần ghi chú “mâu thuẫn” và đánh dấu "Cần làm rõ".  
   - Tiến triển (Progressive): các observation tạo thành một dòng thời gian/logic.  

4. Tree-of-Thought (ToT) phân nhánh  
   - Nhánh 1 – Đã có: Tập dữ liệu đủ để đáp ứng objective.  
   - Nhánh 2 – Cần làm rõ: Có dữ liệu nhưng thiếu chi tiết quan trọng hoặc có mâu thuẫn.  
   - Nhánh 3 – Thiếu: Không có dữ liệu liên quan.  
   - Nhánh 4 – N/A: Slot/Sub-slot không phục vụ mission/objective.  
   - Nhánh 5: Thông tin được user xác nhận không có, bỏ qua, không cung cấp 
5. Counterfactual Thinking  
   - Nếu coi tập observation là ĐỦ → còn thiếu gì để CV hoàn chỉnh hơn?  
   - Nếu coi chưa đủ → cần hỏi/thực hiện thêm Action nào để lấy thông tin còn thiếu?  
   - Nếu thông tin người dùng xác nhận 2 lần trở lên thì cho nó đã hoàn thiện
   - Nếu thông tin người dùng xác nhận không có hoặc bỏ qua thì sub-slot, slot đó bỏ qua
   
6. Đánh giá khả năng bỏ qua (Skip Evaluation)
**Lưu ý**:
   - Nếu thông tin ít quan trọng hoặc user từ chối bổ sung (“không nhớ”, “chỉ có vậy”) → gán "Bỏ qua".

   - Nếu người dùng trả lời rõ ràng “không có” → gán thẳng trạng thái "Bỏ qua", kể cả slot quan trọng.

   - Quy tắc này có tính ưu tiên cao nhất: chỉ cần user nói “không có” thì slot/sub-slot đó sẽ không được yêu cầu làm rõ thêm, và được coi là không tồn tại trong CV.
   - Nếu người dùng xác nhận thông tin như vậy thì cho bỏ qua luôn
7. Kết luận hợp nhất  
   - Sau khi phân tích Action – Observation và mối quan hệ, chọn trạng thái cuối cùng (Đã có / Cần làm rõ / Thiếu / N/A / Bỏ qua).  
   - Ghi rõ observation nào là **nguồn chính**, observation nào chỉ **bổ trợ** hoặc **mâu thuẫn**.  

---

### Định dạng output cho mỗi slot/sub-slot:
- Slot: <tên slot chính>  
- Sub-slot: <tên sub-slot đang xử lý, nếu có; nếu không thì ghi "N/A">  
- Action – Observation Set: <liệt kê các cặp action–observation liên quan>  
- Liên quan tới slot: <mức độ liên quan: trực tiếp / gián tiếp / không liên quan>  
- Quan hệ giữa observations: <bổ sung / trùng lặp / mâu thuẫn / tiến triển>  
- Soi với objective: <giải thích vì sao tập dữ liệu này đã/ chưa đạt yêu cầu>  
- ToT nhánh: <liệt kê 3–4 nhánh>  
- Counterfactual: <nếu coi đủ thì còn gì thiếu, nếu coi chưa đủ thì cần thêm gì>  
- Đánh giá bỏ qua: <có nên bỏ qua không, và tại sao>  
- Kết luận: <Đã có / Cần làm rõ / Thiếu / N/A / Bỏ qua>


## A. Lập kế hoạch (Planning)
Lấy đầu vào ở bước 0
- Với mỗi slot có sub-slot: duyệt tuần tự từng sub-slot theo thứ tự trong required_slots.
- Chỉ chọn đúng 1 sub-slot duy nhất để xử lý trong mỗi lượt.
- Không được xử lý nhiều sub-slot cùng lúc.
- Nếu slot có nhiều sub-slot → phải hoàn thành sub-slot hiện tại (Đã có / Bỏ qua / N/A) trước khi chuyển sang sub-slot kế tiếp.
- Khi tất cả sub-slot của một slot đã hoàn thành → chuyển sang slot kế tiếp trong danh sách.
- Nếu sub-slot chưa hoàn tất (Cần làm rõ / Thiếu) → tiếp tục xử lý sub-slot đó cho đến khi đạt trạng thái cuối cùng.
***Lưu ý***: Thực hiện hành động ưu tiên cho user nhiều hơn:
Ví dụ:
Khách hàng bảo hết thông tin thì bỏ qua luôn


### B. Chia nhỏ vấn đề (Decomposition)
- Nếu slot phức tạp, phân rã thành các sub-problem nhỏ.
- Với mỗi sub-problem: tự suy luận trước → dùng công cụ (có thể hỏi user để lấy input cho tool) → cuối cùng mới hỏi user nội dung trực tiếp.
- Ghép lại thành câu trả lời đầy đủ.

### C. Deliberation (Cân nhắc trước quyết định – Tree-of-Thought + Counterfactual)

1. Đầu tiên, hãy **liệt kê ra ít nhất 4–6 nhánh/cách khác nhau** để giải quyết cho mỗi sub-slot đã chọn:  
   - Với mỗi nhánh phải mô tả **thật chi tiết các bước thực hiện**, bao gồm:  
     * Nếu tự suy luận được → mô tả cách suy luận.  
     * Nếu cần tool → ghi rõ sẽ gọi tool nào, input cụ thể ra sao.  
     * Nếu cần hỏi user → ghi rõ câu hỏi sẽ hỏi.  
       - Đồng thời phân tích rõ:  
         + Mô hình hiện còn **thiếu thông tin gì**.  
         + **Tại sao cần thông tin đó** (liên quan tới objective).  
         + **Mong muốn người dùng cung cấp gì** (ngắn gọn, cụ thể).  
   - Ví dụ:  
     * Nhánh 1: Tự suy luận từ history → điền giá trị.  
     * Nhánh 2: Gọi tool `github_get_user_pygithub[{{"username": "hoivd"}}]` → lấy thông tin repo.  
     * Nhánh 3: Hỏi user: ask_user["Bạn đã sử dụng công nghệ gì trong dự án này? — (Lý do: cần làm rõ tech stack để mô tả kỹ năng theo objective)"].  
     * Nhánh 4: Kết hợp tool + hỏi user (hỏi username trước, sau đó gọi tool).  

2. Với mỗi nhánh, thực hiện **counterfactual prompting**:  
   - Nếu chọn nhánh này thì kết quả sẽ là gì?  
   - Có đạt được `objective` không?  
   - Ưu điểm và nhược điểm so với các nhánh khác?  
   - Có giúp giảm thiểu số lần phải hỏi user không?  

3. So sánh tất cả các nhánh dựa trên tiêu chí:  
   - **Độ chính xác và tin cậy** của dữ liệu thu được.  
   - **Mức độ phù hợp với objective** (có giúp đạt yêu cầu đầy đủ không).  
   - **Tiện lợi cho người dùng**:  
     * Có giảm thiểu số lần phải hỏi user không?  
     * Câu hỏi có ngắn gọn, rõ ràng, dễ trả lời không?  
     * Có tránh lặp lại hoặc gây phiền hà cho user không?  
   - **Chi phí tương tác với user** (ưu tiên càng ít câu hỏi càng tốt).  
   - **Rủi ro sai sót hoặc bỏ sót thông tin**.  

4. Ghi rõ:  
   - Các nhánh đã loại bỏ (và lý do loại).  
   - Nhánh cuối cùng được chọn (và lý do chọn).  
   - Kèm theo **Action cụ thể sẽ được gọi**:  
     * Nếu hỏi user → phải kèm theo câu hỏi **+ giải thích rõ lý do hỏi và mong muốn thông tin**.  
     * Nếu dùng tool → ghi rõ input.  
     * Nếu tự suy luận → ghi giá trị.  

5. Sau đó mới tiến tới bước **Verification** để soi lại nhánh đã chọn trước khi hành động.

# D. Kiểm chứng (Verification mở rộng & chi tiết – Hướng tới tiện lợi cho người dùng)
- Sau khi đề xuất Action, luôn tiến hành bước tự kiểm chứng nghiêm ngặt trước khi thực hiện.
- Đặt ít nhất **7–8 câu hỏi kiểm chứng**, tập trung vào:

1. **Mục tiêu & giá trị**  
   - Action này có trực tiếp giúp **thu thập thông tin từ người dùng** để hoàn thiện slot còn thiếu không?  
   - Có nguy cơ Action chỉ tạo ra dữ liệu **không đến từ người dùng** (giả định/suy diễn) hay không?  
   - Nó có bám sát vào yêu cầu trong `objective` không?  
   - Có giúp giảm số lần hỏi người dùng không cần thiết không?  

2. **Logic & hiệu quả**  
   - Đây có phải cách ngắn nhất, rõ ràng và dễ hiểu nhất đối với người dùng không?  
   - Câu hỏi có tránh được vòng vo, lan man, gây khó hiểu cho user không?  

3. **Nhất quán dữ liệu**  
   - Action có mâu thuẫn với dữ liệu trong `history` không?  
   - Có đảm bảo không làm sai lệch hoặc bóp méo thông tin đã có trước đó không?  

4. **Trùng lặp với lịch sử**  
   - Câu hỏi/action này có bị **trùng lặp** với một câu hỏi đã từng được hỏi trong `history` không?  
   - Nếu có, có thật sự cần hỏi lại để bổ sung chi tiết, hay chỉ lặp lại vô ích?  
   - Có thể diễn đạt câu hỏi khác đi để gợi mở thêm thông tin mới, thay vì lặp lại 100%?  

5. **Độ đầy đủ & độ tin cậy**  
   - Nếu người dùng trả lời, thông tin thu được có đủ chi tiết để đưa vào CV chưa?  
   - Có cần thêm số liệu định lượng, baseline, hoặc ngữ cảnh cụ thể không?  
   - Câu hỏi có khuyến khích user trả lời ngắn gọn nhưng vẫn đủ ý không (đỡ tốn công user)?  

6. **Kết quả kỳ vọng**  
   - Output của Action (câu hỏi hoặc End[…]) có đúng định dạng yêu cầu không?  
   - Có chắc chắn giúp tiến gần hơn tới việc lấp đầy tất cả slot và hoàn thành `objective` không?  

---

- Nếu phát hiện Action **không dẫn đến việc thu thập dữ liệu thật sự từ người dùng** → bắt buộc quay lại bước C (Deliberation) để điều chỉnh Action.  
- Nếu phát hiện Action **bị trùng lặp với history mà không bổ sung giá trị mới** → quay lại bước C để tinh chỉnh câu hỏi.  
- Nếu Action khiến người dùng phải trả lời dài dòng, phức tạp → ưu tiên chỉnh lại cho **dễ hiểu, nhanh gọn, ít tốn sức**.  
- Nếu bất kỳ câu trả lời nào khác cho các câu hỏi trên là **“Không”** → cũng quay lại bước Deliberation.

---



# Nguyên tắc cập nhật khi nhận câu trả lời từ user
- Sau mỗi câu trả lời từ user, bắt buộc quay lại **Bước 0 (Slot/Sub-slot Tracking)** để phân tích lại:  
  + Thông tin nào đã được bổ sung (cập nhật trạng thái = Đã có).  
  + Thông tin nào vẫn còn thiếu (giữ trạng thái = Thiếu hoặc Cần làm rõ).  
- Khi sang **F. Tối ưu Action hỏi user**, phải phản ánh rõ phần đã có và phần còn thiếu.  
  + Không được hỏi lại những gì user đã cung cấp.  
  + Chỉ hỏi đúng phần còn thiếu, gắn chặt với thông tin user vừa trả lời. 
# E. Tối ưu Action hỏi user (User Query Optimization)

Nếu Action cuối cùng được chọn là **hỏi user**, quy trình bắt buộc như sau:
Nếu phải hỏi user → chỉ hỏi đúng một sub-slot đang xử lý.
- Không gộp nhiều sub-slot  khác trong một câu hỏi.

1. **Phân tích trước khi hỏi (ghi rõ trong CoT hoặc trong ask_user)**  
   - Thiếu gì: mô tả cụ thể khoảng trống dữ liệu (thiếu ở mức nào, thiếu phần nào so với objective).  
     *Ví dụ: “Trong dự án A đã có tên và nhiệm vụ, nhưng chưa có công nghệ (tech stack). Vì vậy thiếu thông tin kỹ thuật để chứng minh kỹ năng.”*  
   - Lý do cần hỏi: tại sao thông tin này quan trọng cho objective (liên quan đến kỹ năng, số liệu định lượng, bối cảnh).  
   - Mong muốn user cung cấp: loại dữ liệu cụ thể cần (tên công nghệ, số liệu %, vai trò, kết quả...).  

2. **Sinh câu hỏi cho user**  
   - Câu hỏi ngắn gọn, đúng trọng tâm, phản ánh trực tiếp khoảng trống trên.  

3. **Hướng dẫn trả lời cho user**  
   - Đưa gợi ý cụ thể để user trả lời dễ dàng.  
   - Phải có **ví dụ minh họa chi tiết** dạng câu hoàn chỉnh.  


## Định dạng BẮT BUỘC khi trả lời (mỗi lượt)
'''
**CoT**: 
- [Phân tích lịch sử] <quá trình phân tích>
- [Planning] <slot nào xử lý trước, kế hoạch tổng quan>  
- [Decomposition] <nếu slot phức tạp → liệt kê sub-problem>  
- [Deliberation] <các lựa chọn + ưu/nhược điểm, nhấn mạnh ưu tiên suy luận/tool, hỏi user nếu cần input cho tool hoặc slot>  
- [Verification] <ít nhất 5 câu hỏi kiểm chứng + trả lời ngắn gọn>  
- [Reasoning] <tóm tắt tại sao chọn lựa chọn cuối cùng>  
- [Critique & Self-Challenge] <phản biện>

**Reason**: <1–2 câu vì sao action này là tối ưu (ưu tiên suy luận/tool, hỏi user nếu thật sự cần thiết)>  
**Action**: <tool_name>[{{"input": <dict tham số>}}]
Nếu là action ask_user thì tuân theo:
**Action**: ask_user["Phân tích: <Đoạn phân tích> Mong muốn: <mức độ chi tiết, loại thông tin>. Câu hỏi: <câu hỏi>. Hướng dẫn: <Cho ví dụ minh hoạ>."]
Ví dụ Cho Action:
**Action**: github_get_repos_pygithub[{{"input": {{"username": "hoivd", "per_page": 10}}}}]

- Chỉ chọn **một** Action ở mỗi lượt.
- Nếu phải hỏi user:
  * Chỉ hỏi đúng tham số cần để chạy tool, hoặc đúng phần thiếu cho slot.  
  * Câu hỏi phải ngắn gọn, đúng trọng tâm, không lặp lại thông tin đã có.  
- Khi đủ dữ liệu, dùng **End[<nội dung tổng hợp>]** (đóng gói theo cấu trúc CV-ready). 
'''

Khi tất cả slot đã đủ dữ liệu hoặc được đánh dấu N/A, không còn slot nào thiếu:
'''
**CoT**: 
- [Planning] <hoàn thành>  
- [Decomposition] <không cần nữa>  
- [Deliberation] <không cần nữa>  
- [Verification] <không cần nữa>  
- [Reasoning] <tóm tắt toàn bộ quá trình>  

**Reason**: <đã hoàn tất thu thập, đạt objective>  
**Action**: End[{{"slot1": "...", "slot2": "...", ...}}]  

### Nguyên tắc đặc biệt
- Sau mỗi câu trả lời từ user, quay lại **Bước 0** để cập nhật trạng thái slot.  
- Khi tất cả slot đã đủ dữ liệu hoặc được đánh dấu N/A → End[…].  
- Nếu xác định rằng **objective không thể đạt được** (dữ liệu không đủ và không có cách bổ sung), phải gán:  
  **Action**: End[{{"status": "Mission không khả thi – Bỏ qua"}}]
Lưu ý nếu End thì nếu các phần đã được hoàn thành
'''
"""

        # Gọi LLM
        response = self.llm.invoke([HumanMessage(content=prompt)]).content.strip()
        print(f"\n📤 LLM Output:\n{response}")

        # Dict update cho state
        update = {
            "reAct": {
                "goal": goal,
                "objective": objective,
                "raw_response": response,
            },
            "current_step": "planning_node",
        }

        return update

    
def main():
    
    from dotenv import load_dotenv
    import os
    import json
    
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            api_key=api_key,
        )
    
    state = {
        'current_mission': {
      "name": "Thu thập thông tin cá nhân chi tiết",
      "goal": "Hoàn thiện phần thông tin cá nhân theo yêu cầu của CV chuyên nghiệp.",
      "objective": "Thu thập đầy đủ các thông tin sau: Họ và tên đầy đủ, Số điện thoại, Địa chỉ email chuyên nghiệp, Địa chỉ (thành phố/tỉnh), Liên kết LinkedIn (nếu có), Liên kết GitHub (rất quan trọng).",
      "priority": "high",
    }
            
    }
    from ...tools.git_tools import GitHubToolsManager
    from ...tools.ask_user_tools import AskUserToolsManager
    from ...tools.tool_manager_registry import ToolManagerRegistry

    # Tạo registry và add các manager
    registry = ToolManagerRegistry([
        GitHubToolsManager(),
        AskUserToolsManager(),
    ])
    agent = PlanningNode(llm=llm, tool_registry=registry)
    
    result = agent(state)
    print(json.dumps(result, ensure_ascii=False, indent=2))
if __name__ == "__main__":
    main()
    #