from typing import List

from pydantic import BaseModel, Field


class ClusterSummary(BaseModel):
    cluster_name: str = Field(
        description="Name or identifier of the cluster based on the predominant file type in this cluster"
    )
    main_purpose: str = Field(
        description="Overall purpose of this cluster in the test automation suite"
    )
    primary_file_type: str = Field(
        description="The predominant file type in this cluster"
    )
    secondary_file_types: List[str] = Field(
        description="Other file types found in this cluster"
    )
    key_themes: List[str] = Field(
        description="Main themes or patterns observed across files in this cluster"
    )
    overall_code_quality: str = Field(
        description="General assessment of code quality in this cluster"
    )
    best_practices_summary: str = Field(
        description="Summary of adherence to best practices in this cluster"
    )
    complexity_overview: str = Field(
        description="Overview of code complexity in this cluster"
    )
    maintainability_assessment: str = Field(
        description="Assessment of overall maintainability of code in this cluster"
    )
    strengths: List[str] = Field(description="Key strengths observed in this cluster")
    areas_for_improvement: List[str] = Field(
        description="Main areas for improvement in this cluster, excluding documentation-related issues"
    )
    cluster_recommendations: List[str] = Field(
        description="Key recommendations for improving this cluster as a whole"
    )
