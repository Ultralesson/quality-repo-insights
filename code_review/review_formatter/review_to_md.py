import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

from code_review.parsers import OverallSummary, FileReview
from code_review.review_components.models import ClusterInfo
from code_review.review_formatter.cluster_summary_formatter import (
    format_and_write_cluster_review,
)

from code_review.review_formatter.file_review_formatter import formatted_file_summary
from code_review.review_formatter.overall_summary_formatter import (
    overall_formatted_review,
)


class ReviewToMd:

    @staticmethod
    def format_overall_review(overall_summary: OverallSummary):
        output_dir = "review_output"
        os.makedirs(output_dir, exist_ok=True)
        overall_formatted_review(overall_summary)

    @staticmethod
    async def format_cluster_summaries(cluster_info: List[ClusterInfo]):
        output_dir = "review_output/cluster_reviews"
        os.makedirs(output_dir, exist_ok=True)
        with ThreadPoolExecutor(max_workers=5) as executor:
            loop = asyncio.get_event_loop()
            futures = []
            for cluster in cluster_info:
                future = loop.run_in_executor(
                    executor, format_and_write_cluster_review, cluster
                )
                futures.append(future)

            await asyncio.gather(*futures)

    @staticmethod
    async def format_file_reviews(file_reviews: Dict[str, FileReview]):
        output_dir = "review_output/file_reviews"
        os.makedirs(output_dir, exist_ok=True)
        loop = asyncio.get_event_loop()
        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for file_name, review in file_reviews.items():
                future = loop.run_in_executor(
                    executor,
                    formatted_file_summary,
                    file_name.replace("/", "_"),
                    review,
                )
                futures.append(future)

        await asyncio.gather(*futures)
