from typing import List, Optional

from pydantic import BaseModel

from code_review.parsers.overall_summary import OverallSummary


class Repository(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    tech_stack: Optional[List[str]] = []
    url: Optional[str] = None
    feedback: Optional[OverallSummary] = None
