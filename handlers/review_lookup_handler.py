from handlers.models import RepoInfo
from integrations.supabase.clients import (
    RepositoryTableClient,
    FileInfoTableClient,
)


class ReviewLookupHandler:

    @staticmethod
    def review_exists(repo_path):
        repo = RepositoryTableClient().get_repository(repo_path)
        return len(repo) > 0 and repo[0]["overall_summary"] is not None

    @staticmethod
    def get_review(repo_info: RepoInfo):
        repo = RepositoryTableClient().get_repository(repo_info.repo_path)
        repo_id = repo[0]["id"]
        overall_summary = repo[0]["overall_summary"]

        repo_files = FileInfoTableClient(repo_id).get_repo_files()

        file_reviews = {
            file_info["file_name"]: file_info["file_review"]
            for file_info in repo_files
        }

        return overall_summary, file_reviews
