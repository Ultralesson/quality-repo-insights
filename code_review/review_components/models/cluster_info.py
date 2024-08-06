from typing import Dict

from pydantic import BaseModel

from code_review.parsers import FileReview, ClusterSummary


class ClusterReviewInfo(BaseModel):
    name: str
    summary: ClusterSummary
    file_reviews: Dict[str, FileReview]
