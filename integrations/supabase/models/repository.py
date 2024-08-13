from typing import Optional

from pydantic import BaseModel


class Repository(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    overall_summary: Optional[str] = None
    last_reviewed_commit: Optional[str] = None
    branch: Optional[str] = None
