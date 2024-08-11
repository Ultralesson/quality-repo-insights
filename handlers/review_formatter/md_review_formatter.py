import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

from code_review.parsers import OverallSummary, FileReview
from code_review.review_components.models import ClusterReviewInfo
from handlers.review_formatter.models.cluster_summary_formatter import (
    format_and_write_cluster_review,
)

from handlers.review_formatter.models.file_review_formatter import create_file_review_md
from handlers.review_formatter.models.overall_summary_formatter import (
    get_overall_summary_md,
)


class MDReviewFormatter:
    def __init__(self, repo_id):
        self.__review_folder = f"review_output/{repo_id}"
        os.makedirs(self.__review_folder, exist_ok=True)
        os.makedirs(f"{self.__review_folder}/cluster_reviews", exist_ok=True)
        os.makedirs(f"{self.__review_folder}/file_reviews", exist_ok=True)

    def create_overall_summary_md_file(self, overall_summary: OverallSummary):
        md_content = get_overall_summary_md(overall_summary)
        with open(f"{self.__review_folder}/overall_summary.md", "w") as md_file:
            md_file.write(md_content)

    async def create_cluster_summary_md_files(
        self, cluster_info: List[ClusterReviewInfo]
    ):
        with ThreadPoolExecutor(max_workers=5) as executor:
            loop = asyncio.get_event_loop()
            futures = []
            for cluster in cluster_info:
                future = loop.run_in_executor(
                    executor,
                    format_and_write_cluster_review,
                    cluster,
                    f"{self.__review_folder}/cluster_reviews",
                )
                futures.append(future)

            await asyncio.gather(*futures)

    async def create_file_review_md_files(self, file_reviews: Dict[str, FileReview]):
        loop = asyncio.get_event_loop()
        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for file_name, review in file_reviews.items():
                future = loop.run_in_executor(
                    executor,
                    create_file_review_md,
                    file_name.replace("/", "_"),
                    review,
                    f"{self.__review_folder}/file_reviews",
                )
                futures.append(future)

        await asyncio.gather(*futures)
