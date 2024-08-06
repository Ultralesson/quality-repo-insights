from typing import Optional

from pydantic import BaseModel

from code_review.parsers import ClusterSummary


class Cluster(BaseModel):
    id: Optional[str] = None
    repo_id: str = None
    cluster_name: str = None
    cluster_summary: ClusterSummary = None
