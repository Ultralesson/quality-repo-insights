from typing import List, Optional

from pydantic import BaseModel

from code_review.parsers import CodeReviewSummary


class FileInfo(BaseModel):
    id: Optional[str] = None
    file_name: str = None
    chunks: Optional[List[str]] = None
    review: Optional[CodeReviewSummary] = None
    cluster_id: str = None
    repo_id: str = None
