import operator
from typing import TypedDict, Dict, Annotated, Set

from components.models import FileReview


class RepoAnalysisState(TypedDict):
    repo_path: str
    file_contents: Dict[str, str]
    file_reviews: Dict[str, FileReview]
    processed_files: Annotated[Set[str], operator.or_]
    summary: str
