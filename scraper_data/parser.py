import json
import os
from typing import List, Optional
import re

class Job:
    def __init__(self, jobKey: str, title: str, companyName: str,
                 location: Optional[str], salary: Optional[str],
                 jobUrl: Optional[str], datePublished: Optional[str],
                 isRemote: Optional[bool], rating: Optional[float],
                 numOfCandidates: Optional[int],
                 companyLogoUrl: Optional[str],
                 descriptionText: Optional[str]):
        self.jobKey = jobKey
        self.title = title
        self.companyName = companyName
        self.location = location
        self.salary = salary
        self.jobUrl = jobUrl
        self.datePublished = datePublished
        self.isRemote = isRemote
        self.rating = rating
        self.numOfCandidates = numOfCandidates
        self.companyLogoUrl = companyLogoUrl
        self.descriptionText = descriptionText

    def to_dict(self):
        """Chuyển object thành dict để lưu JSON"""
        return {
            "jobKey": self.jobKey,
            "title": self.title,
            "companyName": self.companyName,
            "location": self.location,
            "salary": self.salary,
            "jobUrl": self.jobUrl,
            "datePublished": self.datePublished,
            "isRemote": self.isRemote,
            "rating": self.rating,
            "numOfCandidates": self.numOfCandidates,
            "companyLogoUrl": self.companyLogoUrl,
            "descriptionText": self.descriptionText,
        }

    def __repr__(self):
        return f"<Job {self.title} @ {self.companyName}>"


class JobParser:
    def __init__(self, output_dir: str = "parsed_jobs"):
        self.output_dir = output_dir
        self.jobs: List[Job] = []
        os.makedirs(self.output_dir, exist_ok=True)

    def parse_from_api_result(self, data: dict):
        job_list = data.get("returnvalue", {}).get("data", [])
        for job in job_list:
            job_obj = Job(
                jobKey=job.get("jobKey"),
                title=job.get("title"),
                companyName=job.get("companyName"),
                location=job.get("location", {}).get("formattedAddressLong"),
                salary=job.get("salary"),
                jobUrl=job.get("jobUrl"),
                datePublished=job.get("datePublished"),
                isRemote=job.get("isRemote"),
                rating=(job.get("rating") or {}).get("rating"),
                numOfCandidates=job.get("numOfCandidates"),
                companyLogoUrl=job.get("companyLogoUrl"),
                descriptionText=job.get("descriptionText"),
            )
            self.jobs.append(job_obj)

    def save_jobs(self):
        """Lưu từng job thành file JSON riêng"""
        for job in self.jobs:
            safe_name = re.sub(r'[^a-zA-Z0-9_-]', "_", f"{job.jobKey}_{job.title}")
            file_path = os.path.join(self.output_dir, f"{safe_name}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(job.to_dict(), f, ensure_ascii=False, indent=2)
        print(f"✅ Saved {len(self.jobs)} jobs → {self.output_dir}")


# --- Ví dụ chạy ---
if __name__ == "__main__":
    parser = JobParser(r"D:\JobHunter\scraper_data\jobs_output\AI_Engineer.json", output_dir="jobs")
    parser.load_and_parse()
    parser.save_jobs()

    print(f"Đã lưu {len(parser.get_jobs())} job vào thư mục 'jobs/'")
