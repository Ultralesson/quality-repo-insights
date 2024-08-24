from components.integrations.supabase.clients import (
    RepositoryTableClient,
    FileInfoTableClient,
)
from components.models import RepoInfo
from config import SUPABASE_KEY, SUPABASE_URL


class ReviewLookupHandler:

    @staticmethod
    def review_exists(repo_path):
        if (
            (SUPABASE_KEY is None or SUPABASE_URL is None)
            or (SUPABASE_KEY.strip() == "")
            or (SUPABASE_URL.strip() == "")
        ):
            return False
        repo = RepositoryTableClient().get_repository(repo_path)
        return len(repo) > 0 and repo[0]["overall_summary"] is not None

    @staticmethod
    def get_review(repo_info: RepoInfo):
        repo = RepositoryTableClient().get_repository(repo_info.repo_path)
        repo_id = repo[0]["id"]
        overall_summary = repo[0]["overall_summary"]

        repo_files = FileInfoTableClient(repo_id).get_repo_files()

        file_reviews = {
            file_info["file_name"]: file_info["file_review"] for file_info in repo_files
        }

        return overall_summary, file_reviews
