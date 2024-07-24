from typing import List

from pydantic import BaseModel, Field


class ClusterSummary(BaseModel):
    main_theme: str = Field(description="The main theme or purpose of this cluster of files")
    key_points: List[str] = Field(description="List of key points or observations about the cluster")
    common_issues: List[str] = Field(description="Common issues or areas for improvement across the cluster")
    strengths: List[str] = Field(description="Strengths or positive aspects of the code in this cluster")
    recommendations: List[str] = Field(description="Recommendations for improving the code in this cluster")
