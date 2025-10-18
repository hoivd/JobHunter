from typing import List
from scraper import IndeedScraper
from parser import JobParser


class JobApp:
    def __init__(self, api_key: str):
        self.scraper = IndeedScraper(api_key)
        self.parser = JobParser()

    def run(self, job_titles: List[str], location="Ho Chi Minh"):
        for title in job_titles:
            print(f"🔎 Searching for: {title}")
            raw_data = self.scraper.search_job(job_title=title, location=location)
            self.parser.parse_from_api_result(raw_data)
        self.parser.save_jobs()


# ----------------- Demo -----------------
if __name__ == "__main__":
    api_key = "c4e8a5a7a1msh2ea146d85e4a069p1b7c07jsnc7cd14116b5b"  # ⚠️ Thay bằng key thật
    job_titles = ["AI Engineer", "Data Scientist", "Python Developer"]

    app = JobApp(api_key)
    app.run(job_titles, location="Ho Chi Minh")