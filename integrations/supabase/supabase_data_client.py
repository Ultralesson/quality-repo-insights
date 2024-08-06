import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

from code_review.parsers import OverallSummary
from code_review.review_components.models import ClusterReviewInfo
from integrations.supabase.clients import (
    ClusterTableClient,
    FileInfoTableClient,
    RepositoryTableClient,
)
from integrations.supabase.models import Cluster, FileInfo, Repository


class SupabaseDataClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SupabaseDataClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, repo_id):
        if not hasattr(self, "_initialized"):
            self.__repository_table_client = RepositoryTableClient()
            self.__cluster_table_client = ClusterTableClient(repo_id)
            self.__file_info_table_client = FileInfoTableClient(repo_id)
            self.__repo_id = repo_id
            self.__supabase_client_lock = threading.Lock()
            self._initialized = True

    async def add_cluster_and_files_to_db(self, cluster_record: list[ClusterReviewInfo]):
        loop = asyncio.get_running_loop()
        futures = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            for cluster in cluster_record:
                future = loop.run_in_executor(
                    executor, self.__add_cluster_and_file_info, cluster
                )
                futures.append(future)

            await asyncio.gather(*futures)

    def __add_cluster_and_file_info(self, cluster: ClusterReviewInfo):
        with self.__supabase_client_lock:
            cluster_record = self.__cluster_table_client.add_cluster(
                Cluster(
                    repo_id=self.__repo_id,
                    cluster_name=cluster.name,
                    cluster_summary=cluster.summary,
                )
            )

            for file_name, review in cluster.file_reviews.items():
                self.__file_info_table_client.add_file_info(
                    FileInfo(
                        file_name=file_name,
                        repo_id=self.__repo_id,
                        file_review=review,
                        cluster_id=cluster_record[0]["id"],
                    )
                )

    def add_overall_review_to_db(self, review: OverallSummary):
        self.__repository_table_client.update_repository(
            data=Repository(overall_summary=review), id=self.__repo_id
        )
