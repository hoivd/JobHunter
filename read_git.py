import os
from dotenv import load_dotenv
from github import Github

# Load biến môi trường
load_dotenv()
gh_token = os.getenv("GITHUB_TOKEN")

# Kết nối GitHub
g = Github(gh_token)
repo = g.get_repo("hoivd/facebook_scraper")  # thay bằng repo bạn muốn

# Lấy README
readme = repo.get_readme().decoded_content.decode("utf-8")

print(readme)