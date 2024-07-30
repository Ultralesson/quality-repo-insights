from typing import List, Dict
from pydantic import BaseModel, Field


class OverallSummary(BaseModel):
    project_overview: str = Field(description="A high-level overview of the entire project based on all clusters")
    main_themes: List[str] = Field(description="List of main themes identified across all clusters")
    key_findings: List[str] = Field(
        description="List of the most important observations or findings across all clusters")
    common_issues: Dict[str, List[str]] = Field(
        description="Common issues grouped by category (e.g., 'Code Quality', 'Performance', 'Security')")
    overall_strengths: List[str] = Field(description="List of overall strengths of the project")
    priority_recommendations: List[str] = Field(
        description="List of high-priority recommendations for the entire project")
    cluster_highlights: Dict[str, Dict[str, str]] = Field(
        description="Brief highlights for each cluster, including main theme and top strength/issue")
    complexity_assessment: str = Field(description="Overall assessment of code complexity across the project")
    tools_and_frameworks: Dict[str, str] = Field(
        description="Overview of main tools and frameworks used, with brief assessment")
    next_steps: List[str] = Field(description="Suggested next steps or areas for focused improvement")

    def to_string(self):
        return (
            f"Project Overview:\n{self.project_overview}\n\n"
            f"Main Themes:\n{'.'.join(self.main_themes)}\n\n"
            f"Key Findings:\n{'\n'.join(self.key_findings)}\n\n"
            f"Common Issues:\n{'\n'.join(self.common_issues)}\n\n"
            f"Overall Strengths:\n{'\n'.join(self.overall_strengths)}\n\n"
            f"Recommendations:\n{'\n'.join(self.priority_recommendations)}\n\n"
            f"Complexity Assessment:\n{self.complexity_assessment}\n\n"
            f"Next Steps:\n{'\n'.join(self.next_steps)}\n\n"
        )
