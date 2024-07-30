from typing import List

from pydantic import BaseModel, Field


class ClusterSummary(BaseModel):
    main_theme: str = Field(
        description="The primary purpose or function of this cluster within the test automation framework")

    key_points: List[str] = Field(description="List of key points or observations about the code in the cluster")

    tools_and_frameworks: str = Field(description="Correct Usage of the tools and frameworks used in this cluster")

    code_quality: str = Field(
        description="Summary of code quality across the cluster, including common strengths and areas for improvement")

    best_practices: str = Field(description="Best practices consistently followed in this cluster")

    common_issues: List[str] = Field(description="Recurring issues or patterns that need attention across the cluster")

    maintainability: str = Field(description="Overall assessment of the maintainability of the code in this cluster")

    recommendations: List[str] = Field(description="Specific recommendations for improving the cluster as a whole")

    complexity_assessment: str = Field(description="Overall assessment of code complexity in this cluster")

    def to_string(self):
        return (
            f"Main Theme: {self.main_theme}\n"
            f"Key Points: {', '.join(self.key_points)}\n"
            f"Tools and Frameworks: {self.tools_and_frameworks}\n"
            f"Code Quality: {self.code_quality}\n"
            f"Best Practices: {self.best_practices}"
            f"Common Issues: {', '.join(self.common_issues)}\n"
            f"Maintainability: {self.maintainability}\n"
            f"Recommendations: {', '.join(self.recommendations)}\n"
            f"Complexity Assessment: {self.complexity_assessment}"
        )
