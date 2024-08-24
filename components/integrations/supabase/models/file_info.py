from typing import Optional

from pydantic import BaseModel

from components.models import FileReview


class FileInfo(BaseModel):
    id: Optional[str] = None
    file_name: str = None
    file_review: FileReview = None
    repo_id: str = None
