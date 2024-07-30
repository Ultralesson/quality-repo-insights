from typing import List, Dict
from pydantic import BaseModel, Field


class OverallSummary(BaseModel):
    project_overview: str = Field(description="High-level overview of the entire test automation project")
    main_clusters: List[str] = Field(description="List of main clusters identified in the project")
    key_strengths: List[str] = Field(description="Key strengths of the overall test automation suite")
    primary_concerns: List[str] = Field(description="Primary concerns or areas needing improvement across the project")
    code_quality_assessment: str = Field(description="Overall assessment of code quality across all clusters")
    best_practices_adherence: str = Field(description="Summary of adherence to best practices across the project")
    complexity_evaluation: str = Field(description="Evaluation of overall code complexity in the project")
    maintainability_overview: str = Field(description="Overview of code maintainability across all clusters")
    cross_cluster_patterns: List[str] = Field(description="Patterns or issues observed across multiple clusters")
    high_priority_recommendations: List[str] = Field(description="High-priority recommendations for the entire project")
    next_steps: List[str] = Field(description="Suggested next steps for improving the test automation suite")
