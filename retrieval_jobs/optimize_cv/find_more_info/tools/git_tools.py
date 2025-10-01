from langchain.tools import tool
from pydantic import BaseModel
from github import Github
from dotenv import load_dotenv
import os

from .base_tools import BaseToolsManager  # import lớp cha

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
gh = Github(GITHUB_TOKEN)


class GitHubToolsManager(BaseToolsManager):
    def _build_tools(self):
        """Định nghĩa các tool cho GitHub."""

        class ListFilesInput(BaseModel):
            owner: str
            repo: str
            path: str = ""   # mặc định root
            ref: str = "main"  # nhánh mặc định

        @tool("github_list_files_pygithub")
        def github_list_files_pygithub(input: ListFilesInput) -> list:
            """
            Liệt kê danh sách file và thư mục trong repository GitHub.
            - Dùng khi cần biết cấu trúc repo hoặc các file có trong thư mục.
            - Input: owner, repo, path (tùy chọn), ref (nhánh, mặc định main).
            - Output: list item {name, path, type=file/dir}.
            """
            try:
                repository = gh.get_repo(f"{input.owner}/{input.repo}")
                contents = repository.get_contents(input.path, ref=input.ref)
                result = []
                for c in contents:
                    result.append({"name": c.name, "path": c.path, "type": c.type})
                return result
            except Exception as e:
                return {"error": str(e)}

        class ReadFileInput(BaseModel):
            owner: str
            repo: str
            path: str
            ref: str = "main"

        @tool("github_read_file_pygithub")
        def github_read_file_pygithub(input: ReadFileInput) -> dict:
            """
            Đọc nội dung một file văn bản nhỏ trong repository GitHub.
            - Dùng khi cần lấy nội dung code, README, config...
            - Input: owner, repo, path (file bắt buộc), ref (nhánh, mặc định main).
            - Output: dict {name, path, content (string)}.
            """
            try:
                repository = gh.get_repo(f"{input.owner}/{input.repo}")
                file_content = repository.get_contents(input.path, ref=input.ref)
                import base64
                content = base64.b64decode(file_content.content).decode("utf-8", errors="ignore")
                return {"name": file_content.name, "path": file_content.path, "content": content}
            except Exception as e:
                return {"error": str(e)}

        @tool("github_get_user_pygithub")
        def github_get_user_pygithub(username: str) -> dict:
            """
            Lấy thông tin chi tiết của một GitHub user.
            - Dùng khi cần biết hồ sơ user: tên, số repo, followers, bio...
            - Input: username (tên đăng nhập GitHub).
            - Output: dict thông tin cơ bản của user.
            """
            try:
                user = gh.get_user(username)
                return {
                    "login": user.login,
                    "name": user.name,
                    "public_repos": user.public_repos,
                    "followers": user.followers,
                    "following": user.following,
                    "url": user.html_url,
                    "company": user.company,
                    "location": user.location,
                    "bio": user.bio,
                    "created_at": str(user.created_at),
                }
            except Exception as e:
                return {"error": str(e)}

        class ReposInput(BaseModel):
            username: str
            per_page: int = 5

        @tool("github_get_repos_pygithub")
        def github_get_repos_pygithub(input: ReposInput) -> list:
            """
            Lấy danh sách repository công khai của một GitHub user.
            - Dùng khi cần biết user có những repo nào.
            - Input: username, per_page (số repo cần lấy).
            - Output: list ["owner/repo1", "owner/repo2", ...].
            """
            try:
                user = gh.get_user(input.username)
                repos = user.get_repos()[: input.per_page]
                return [repo.full_name for repo in repos]
            except Exception as e:
                return {"error": str(e)}

        class IssuesInput(BaseModel):
            owner: str
            repo: str
            state: str = "open"
            per_page: int = 5

        @tool("github_get_issues_pygithub")
        def github_get_issues_pygithub(input: IssuesInput) -> list:
            """
            Lấy danh sách issues trong một repository GitHub.
            - Dùng khi cần kiểm tra các vấn đề đang mở/đóng.
            - Input: owner, repo, state (open/closed/all), per_page.
            - Output: list {title, url}.
            """
            try:
                repository = gh.get_repo(f"{input.owner}/{input.repo}")
                issues = repository.get_issues(state=input.state)[: input.per_page]
                return [{"title": i.title, "url": i.html_url} for i in issues]
            except Exception as e:
                return {"error": str(e)}

        class PRsInput(BaseModel):
            owner: str
            repo: str
            state: str = "open"
            per_page: int = 5

        @tool("github_get_pull_requests_pygithub")
        def github_get_pull_requests_pygithub(input: PRsInput) -> list:
            """
            Lấy danh sách pull requests trong một repository GitHub.
            - Dùng khi cần biết repo có PR nào đang mở, đã đóng, hoặc tất cả.
            - Input: owner, repo, state (open/closed/all), per_page.
            - Output: list {title, url}.
            """
            try:
                repository = gh.get_repo(f"{input.owner}/{input.repo}")
                pulls = repository.get_pulls(state=input.state)[: input.per_page]
                return [{"title": pr.title, "url": pr.html_url} for pr in pulls]
            except Exception as e:
                return {"error": str(e)}

        class SearchRepoInput(BaseModel):
            query: str
            per_page: int = 5

        @tool("github_search_repos_pygithub")
        def github_search_repos_pygithub(input: SearchRepoInput) -> list:
            """
            Tìm kiếm repository trên GitHub theo từ khóa.
            - Dùng khi cần tìm repo theo công nghệ, chủ đề hoặc tên.
            - Input: query (từ khóa), per_page (số repo cần lấy).
            - Output: list {name: 'owner/repo', stars: int}.
            """
            try:
                repos = gh.search_repositories(query=input.query)[: input.per_page]
                return [{"name": r.full_name, "stars": r.stargazers_count} for r in repos]
            except Exception as e:
                return {"error": str(e)}

        return {
            "github_get_user_pygithub": github_get_user_pygithub,
            "github_get_repos_pygithub": github_get_repos_pygithub,
            "github_get_issues_pygithub": github_get_issues_pygithub,
            "github_get_pull_requests_pygithub": github_get_pull_requests_pygithub,
            "github_search_repos_pygithub": github_search_repos_pygithub,
            "github_list_files_pygithub": github_list_files_pygithub,
            "github_read_file_pygithub": github_read_file_pygithub,
        }

if __name__ == "__main__":
    manager = GitHubToolsManager()
    print("📌 Tools text:\n")
    print(manager.get_tools_text())