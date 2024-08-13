import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

from handlers.models import FileReview
from handlers.models import RepoInfo
from integrations.supabase.clients import (
    FileInfoTableClient,
    RepositoryTableClient,
)
from integrations.supabase.models import FileInfo, Repository


class SupabaseDataClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SupabaseDataClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.__repository_table_client = RepositoryTableClient()
            self.__supabase_client_lock = threading.Lock()
            self._initialized = True

    @staticmethod
    def add_repository(repo_info: RepoInfo) -> str:
        repo = RepositoryTableClient().add_repository(
            Repository(
                name=repo_info.name,
                url=repo_info.repo_path,
                last_reviewed_commit=repo_info.head_commit_sha,
                branch=repo_info.branch,
            )
        )

        return repo["id"]

    async def add_files_to_db(self, repo_id: str, file_reviews: dict[str, FileReview]):
        loop = asyncio.get_running_loop()
        futures = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            for file_name, review in file_reviews.items():
                future = loop.run_in_executor(
                    executor, self.__add_file_info, repo_id, file_name, review
                )
                futures.append(future)

            await asyncio.gather(*futures)

    def __add_file_info(self, repo_id: str, file_name: str, review: FileReview):
        with self.__supabase_client_lock:
            file_info_table_client = FileInfoTableClient(repo_id)

            file_info_table_client.add_file_info(
                FileInfo(file_name=file_name, repo_id=repo_id, file_review=review)
            )

    def add_overall_review_to_db(self, repo_id, review):
        self.__repository_table_client.update_repository(
            data=Repository(overall_summary=review), repo_id=repo_id
        )
