from github import Github
from config.settings import Settings

class GithubTool:
    def __init__(self, repo_name: str = "hoivd/facebook_scraper"):
        self.g = Github(Settings.GITHUB_TOKEN)
        self.repo = self.g.get_repo(repo_name)

    def read_file(self, path: str) -> str:
        try:
            file_content = self.repo.get_contents(path)
            return file_content.decoded_content.decode("utf-8")
        except Exception as e:
            return f"Lỗi khi đọc file {path}: {e}"

    def list_files(self, path: str = "") -> str:
        try:
            contents = self.repo.get_contents(path)
            return "\n".join([c.path for c in contents])
        except Exception as e:
            return f"Lỗi khi liệt kê file {path}: {e}"