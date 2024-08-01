import threading
from typing import Dict, List

from code_review.parsers import CodeReviewSummary, OverallSummary
from database.supabase.clients import (
    ClusterTableClient,
    FileInfoTableClient,
    RepositoryTableClient,
)
from database.supabase.models import Cluster, FileInfo, Repository


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
            self.__cluster_db_data = {}
            self._initialized = True

    def add_clusters_and_files_to_db(
        self, cluster_files: Dict[str, List[Dict[str, Dict]]]
    ):
        for cluster_name, cluster_files_info in cluster_files.items():
            cluster_info = self.__cluster_table_client.add_cluster(
                Cluster(repo_id=self.__repo_id, cluster_name=str(cluster_name))
            )

            self.__cluster_db_data[cluster_name] = {
                "cluster_id": cluster_info[0]["id"],
                "files": [],
            }

            for file_info in cluster_files_info:
                for file_name, file_content in file_info.items():
                    file_info_record = self.__file_info_table_client.add_file_info(
                        FileInfo(
                            file_name=file_name,
                            repo_id=self.__repo_id,
                            chunks=file_content["chunks"],
                            cluster_id=cluster_info[0]["id"],
                        )
                    )

                    self.__cluster_db_data[cluster_name]["files"].append(
                        {
                            "file_name": file_name,
                            "file_info_id": file_info_record[0]["id"],
                        }
                    )

    def add_file_reviews_to_db(
        self, cluster_file_reviews: Dict[str, Dict[str, CodeReviewSummary]]
    ):
        for cluster_name, file_reviews in cluster_file_reviews.items():
            cluster_db_data = self.__cluster_db_data[cluster_name]

            for file_name, review in file_reviews.items():
                for file in cluster_db_data["files"]:
                    if file["file_name"] == file_name:
                        self.__file_info_table_client.update_file_info(
                            data=FileInfo(review=review, file_name=file_name),
                            file_id=file["file_info_id"],
                        )
                        break

    def add_cluster_summary_to_db(self, cluster_summaries: Dict[str, Dict]):
        for cluster_name, cluster_info in cluster_summaries.items():
            cluster_id = self.__cluster_db_data[cluster_name]["cluster_id"]
            self.__cluster_table_client.update_cluster(
                data=Cluster(feedback_summary=cluster_info["summary"]),
                cluster_id=cluster_id,
            )

    def add_overall_review_to_db(self, review: OverallSummary):
        self.__repository_table_client.update_repository(
            data=Repository(feedback=review), id=self.__repo_id
        )
