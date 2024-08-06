from typing import List, Dict

from code_review.parsers import FileReview
from code_review.review_components.models import ClusterReviewInfo
from handlers.models.review import Review
from integrations.supabase.clients import (
    RepositoryTableClient,
    ClusterTableClient,
    FileInfoTableClient,
)
from handlers.models import RepoInfo


class ReviewLookupHandler:

    @staticmethod
    def review_exists(repo_path):
        repo = RepositoryTableClient().get_repository(repo_path)
        return len(repo) > 0

    @staticmethod
    def get_review(repo_info: RepoInfo) -> Review:
        repo = RepositoryTableClient().get_repository(repo_info.repo_path)
        repo_id = repo[0]["id"]
        overall_summary = repo[0]["overall_summary"]

        clusters = ClusterTableClient(repo_id).get_all_clusters()

        cluster_reviews: List[ClusterReviewInfo] = []
        file_reviews: Dict[str, FileReview] = {}

        for cluster in clusters:
            cluster_id = cluster["id"]
            cluster_files = FileInfoTableClient(repo_id).get_cluster_files(cluster_id)
            cluster_file_reviews = {
                file_info["file_name"]: file_info["file_review"]
                for file_info in cluster_files
            }
            file_reviews.update(cluster_file_reviews)
            cluster_reviews.append(
                ClusterReviewInfo(
                    name=cluster["cluster_name"],
                    summary=cluster["cluster_summary"],
                    file_reviews=cluster_file_reviews,
                )
            )

        return Review(
            repo_id=repo_id,
            overall_summary=overall_summary,
            cluster_reviews=cluster_reviews,
            file_reviews=file_reviews,
        )
