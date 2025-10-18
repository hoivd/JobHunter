# 🧠 JobHunter — Indeed Scraper & Parser

Dự án này giúp bạn **tự động thu thập và phân tích dữ liệu việc làm** từ Indeed thông qua **RapidAPI - Indeed Scraper API**.  
Project gồm 3 phần chính: **Scraper**, **Parser**, và **App** để chạy tổng thể.

---

## 📁 Cấu trúc thư mục

```
project_root/
│
├── parsed_jobs/          # Thư mục lưu dữ liệu đã parse ra từng job
│
├── app.py                # Chương trình chính — phối hợp Scraper + Parser
├── parser.py             # Lớp xử lý và lưu dữ liệu job từ API
├── scraper.py            # Lớp thu thập dữ liệu job từ Indeed API
└── README.md             # Tài liệu hướng dẫn
```

---

## ⚙️ 1. Mô tả chức năng

### **`scraper.py`**
- Chứa lớp `IndeedScraper` chịu trách nhiệm **gửi request API** đến Indeed.
- Mỗi lần tìm kiếm job theo `job_title`, kết quả được lưu lại thành file JSON riêng.
- Các hàm chính:
  - `search_job()` → Gửi request tìm job.
  - `save_job_result()` → Lưu kết quả ra file.
  - `search_jobs()` → Chạy nhiều job titles cùng lúc và tự lưu.

---

### **`parser.py`**
- Chứa lớp `JobParser` và `Job`.
- Chuyển dữ liệu thô từ API thành **object rõ ràng** (title, company, salary, url, v.v.).
- Lưu từng job ra file JSON riêng trong thư mục `parsed_jobs/`.
- Các hàm chính:
  - `parse_from_api_result()` → Chuyển dữ liệu từ API sang object `Job`.
  - `save_jobs()` → Lưu từng job thành file JSON.

---

### **`app.py`**
- Là **entry point chính**.
- Dùng để chạy toàn bộ quy trình:  
  Gọi `IndeedScraper` → Lấy dữ liệu → Gọi `JobParser` → Lưu kết quả.
- Class chính: `JobApp`.

---

## 🚀 2. Cách chạy chương trình

### **Yêu cầu**
- Python 3.8 trở lên  
- Có sẵn thư viện chuẩn (không cần cài thêm ngoài requests/http.client)
- Có tài khoản RapidAPI và key từ [Indeed Scraper API](https://rapidapi.com/)

---

### **Các bước thực hiện**

1. **Clone hoặc tải project về:**
   ```bash
   git clone https://github.com/yourusername/jobhunter.git
   cd jobhunter
   ```

2. **Thêm API key của bạn vào file `app.py`:**
   ```python
   api_key = "YOUR_RAPIDAPI_KEY"
   ```

3. **Chạy chương trình:**
   ```bash
   python app.py
   ```

4. **Kết quả:**
   - Các file JSON thô được lưu trong thư mục `jobs_output/`.
   - Các file JSON đã parse từng job được lưu trong thư mục `parsed_jobs/`.

---

## 🧩 3. Ví dụ kết quả đầu ra

Ví dụ file `parsed_jobs/AI_Engineer.json`:

```json
{
  "jobKey": "abc123",
  "title": "AI Engineer",
  "companyName": "OpenAI",
  "location": "Ho Chi Minh City, Vietnam",
  "salary": "30,000,000 - 50,000,000 VND",
  "jobUrl": "https://vn.indeed.com/viewjob?jk=abc123",
  "datePublished": "2025-10-18",
  "isRemote": true,
  "rating": 4.5,
  "numOfCandidates": 20,
  "companyLogoUrl": "https://company.com/logo.png",
  "descriptionText": "Develop AI models and pipelines..."
}
```

---

## 🧠 4. Luồng hoạt động tổng quát

```mermaid
graph TD
    A[app.py] -->|call| B[IndeedScraper]
    B -->|fetch data| C[RapidAPI - Indeed]
    C -->|return raw JSON| B
    B --> D[save_job_result()]
    A -->|pass raw data| E[JobParser]
    E -->|parse jobs| F[Job Objects]
    F -->|save| G[parsed_jobs/*.json]
```

---

## ✅ 5. Ưu điểm
- Mã nguồn tách biệt rõ: **Scraping**, **Parsing**, **App runner**
- Dễ mở rộng để thêm các website khác.
- Tự động lưu dữ liệu từng job để phân tích sau này.

---

## 🧾 6. Giấy phép
MIT License © 2025 — Bạn có thể tự do chỉnh sửa và mở rộng.
