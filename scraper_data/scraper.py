import http.client
import json
import os
import re

class IndeedScraper:
    def __init__(self, api_key, host="indeed-scraper-api.p.rapidapi.com"):
        self.api_key = api_key
        self.host = host

    def search_job(self, job_title, location="Ho Chi Minh", radius="50", sort="relevance", from_days="7", country="vn", max_rows=10):
        """
        Gửi request tìm job cho 1 job_title
        """
        conn = http.client.HTTPSConnection(self.host)

        payload = {
            "scraper": {
                "maxRows": max_rows,
                "query": job_title,
                "location": location,
                "radius": radius,
                "sort": sort,
                "fromDays": from_days,
                "country": country
            }
        }

        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.host,
            "Content-Type": "application/json"
        }

        conn.request("POST", "/api/job", json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))

    def save_job_result(self, job, data, folder="jobs_output"):
        """
        Lưu kết quả 1 job vào file JSON riêng
        """
        os.makedirs(folder, exist_ok=True)
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', "_", job)
        filename = os.path.join(folder, f"{safe_name}.json")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved {job} → {filename}")

    def search_jobs(self, job_list, location="Ho Chi Minh"):
        """
        Gửi request cho cả danh sách job_titles.
        Sau mỗi job thì lưu file luôn.
        """
        results = {}
        for job in job_list:
            print(f"🔎 Searching for: {job}")
            data = self.search_job(job_title=job, location=location)
            results[job] = data
            # lưu ngay khi xong job này
            self.save_job_result(job, data, folder="jobs_output")
        return results


# ------------------- Demo -------------------
if __name__ == "__main__":
    api_key = "c4e8a5a7a1msh2ea146d85e4a069p1b7c07jsnc7cd14116b5b"  # ⚠️ thay bằng key thật
    scraper = IndeedScraper(api_key)

    job_titles = ["AI Engineer", "Data Scientist", "Python Developer"]

    results = scraper.search_jobs(job_titles, location="Ho Chi Minh")
