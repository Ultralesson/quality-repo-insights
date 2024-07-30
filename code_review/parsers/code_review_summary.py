from typing import List, Dict

from pydantic import BaseModel, Field


class CodeReviewSummary(BaseModel):
    main_purpose: str = Field(
        description="Brief description of the file's main purpose in the context of test automation or quality assurance")

    key_points: List[str] = Field(description="List of key points or observations about the code")

    file_type: str = Field(
        description="Type of file (e.g., Test Class, Page Object, Utility, Configuration)"
    )

    tools_and_libraries: Dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary of tools/libraries used (e.g., Selenium, Appium, RestAssured) and brief assessment of their usage in this file"
    )

    code_quality: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Evaluation of code quality, including strengths and areas for improvement specific to this file"
    )

    best_practices: List[str] = Field(
        description="List of adherence to or deviations from best practices in test automation or quality assurance observed in this file"
    )

    complexity_assessment: Dict[str, str] = Field(
        default_factory=dict,
        description="Assessment of code complexity, including cyclomatic complexity if applicable, and qualitative evaluation"
    )

    maintainability: str = Field(
        description="Assessment of code maintainability and readability for this specific file"
    )

    file_organization: str = Field(
        description="Assessment of how well the content within this file is organized and structured"
    )

    recommendations: List[str] = Field(
        description="Specific recommendations for improving this file"
    )

    def to_string(self):
        return (
            f"Main Purpose: {self.main_purpose}\n"
            f"file_type: {self.file_type}\n"
            f"Key Points: {', '.join(self.key_points)}\n"
            f"Tools and Libraries: {self.tools_and_libraries}\n"
            f"Code Quality: {self.code_quality}\n"
            f"Best Practices: {self.best_practices}\n"
            f"Complexity Assessment: {self.complexity_assessment}\n"
            f"maintainability: {self.maintainability}\n"
            f"file_organization: {self.file_organization}\n"
            f"recommendations: {self.recommendations}\n"
        )
