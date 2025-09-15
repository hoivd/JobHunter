# 🤖 GitHub Agent với LangChain + Gemini

Đây là một ví dụ về **Conversational Agent** sử dụng:
- [LangChain](https://www.langchain.com/)  
- [Google Gemini](https://ai.google.dev/) (qua `langchain-google-genai`)  
- [GitHub API](https://docs.github.com/en/rest) (qua `PyGithub`)  

Agent này có thể:
- 📂 Liệt kê file trong một repo GitHub  
- 📖 Đọc nội dung file (ví dụ: `README.md`)  
- 🛑 Kết thúc hội thoại khi bạn nói *cảm ơn*, *muốn dừng*, *thoát*...  
- 💬 Giao tiếp hội thoại nhiều lượt (có memory)  

---

## ⚙️ 1. Cài đặt

```bash

# Tạo môi trường ảo (khuyến nghị)
conda create -n github-agent python=3.11
conda activate github-agent

# Cài thư viện
pip install -r requirements.txt
```

**`requirements.txt`** (ví dụ):
```
langchain
langchain-google-genai
PyGithub
python-dotenv
```

---

## 🔑 2. Cấu hình API Key

Tạo file `.env` trong thư mục gốc và thêm:

```env
GOOGLE_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_token
```

- **GOOGLE_API_KEY**: API key từ [Google AI Studio](https://makersuite.google.com/app/apikey).  
- **GITHUB_TOKEN**: [Personal Access Token](https://github.com/settings/tokens) từ GitHub (nếu repo private thì cần scope `repo`).  

---

## 🚀 3. Cách chạy

Chạy script hội thoại:

```bash
python conversation_git.py
```

---

## 💬 4. Ví dụ hội thoại

```text
🤖 Agent sẵn sàng! Bạn có thể chat, gõ 'cảm ơn' hay 'muốn dừng' để kết thúc.

Bạn: Repo này có những file gì ở thư mục gốc?
🤖 Agent: DIR: .github
           FILE: README.md
           FILE: setup.py
           ...

Bạn: Hãy đọc README.md và tóm tắt nội dung cho tôi.
🤖 Agent: README mô tả repo facebook_scraper là công cụ thu thập dữ liệu từ Facebook...

Bạn: Cảm ơn, dừng lại.
🤖 Agent: Cảm ơn bạn, mình sẽ dừng ở đây 👋
```

---

## 📌 5. Các Tool hỗ trợ

- **ReadFile** → Đọc nội dung file từ repo.  
- **ListFiles** → Liệt kê file/thư mục trong repo (dùng `'/'` để chỉ thư mục gốc).  
- **StopConversation** → Dùng khi muốn kết thúc hội thoại.  

---

## ✅ 6. Lưu ý

- Mặc định code đang trỏ vào repo: `hoivd/facebook_scraper`.  
- Bạn có thể thay đổi repo bằng cách sửa dòng:
  ```python
  repo = g.get_repo("owner/repo-name")
  ```
- Nếu repo private, token GitHub phải có đủ quyền.  
- Nếu hội thoại dài → có thể thay `ConversationBufferMemory` bằng `ConversationSummaryMemory` để tiết kiệm token.
