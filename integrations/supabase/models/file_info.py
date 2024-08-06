from typing import List, Optional

from pydantic import BaseModel

from code_review.parsers import FileReview


class FileInfo(BaseModel):
    id: Optional[str] = None
    file_name: str = None
    file_review: FileReview = None
    cluster_id: str = None
    repo_id: str = None
