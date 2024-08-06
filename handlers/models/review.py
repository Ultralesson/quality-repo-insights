from typing import List, Dict

from pydantic import BaseModel

from code_review.parsers import OverallSummary, FileReview
from code_review.review_components.models import ClusterReviewInfo


class Review(BaseModel):
    repo_id: str = None
    overall_summary: OverallSummary = None
    cluster_reviews: List[ClusterReviewInfo] = []
    file_reviews: Dict[str, FileReview] = {}
