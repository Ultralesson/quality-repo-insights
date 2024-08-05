from typing import List, Optional

from pydantic import BaseModel

from code_review.parsers.overall_summary import OverallSummary


class Repository(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    overall_summary: Optional[OverallSummary] = None
