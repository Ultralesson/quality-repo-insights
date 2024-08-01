from typing import Dict

from code_review.parsers import OverallSummary
from code_review.review_formatter.cluster_summary_formatter import format_cluster_summaries
from code_review.review_formatter.file_review_formatter import formatted_file_summary
from code_review.review_formatter.overall_summary_formatter import overall_formatted_review


class ReviewToMd:

    @staticmethod
    def format_overall_review(overall_summary: OverallSummary):
        overall_formatted_review(overall_summary)

    @staticmethod
    def format_cluster_summaries(summaries: Dict[str, Dict]):
        format_cluster_summaries(summaries)

    @staticmethod
    def format_file_reviews(file_reviews: Dict[str, Dict]):
        for _, files in file_reviews.items():
            for file_name, review in files.items():
                formatted_file_summary(file_name.replace("/", "_"), review)
