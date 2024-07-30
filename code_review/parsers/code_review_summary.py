from typing import List, Dict

from pydantic import BaseModel, Field


class CodeReviewSummary(BaseModel):
    main_purpose: str = Field(
        description="Brief description of the file's main purpose in the context of test automation or quality assurance"
    )
    key_points: List[str] = Field(description="List of key points or observations about the code")
    file_type: str = Field(description="Type of file (e.g., Test Class, Page Object, Utility, Configuration)")
    code_quality: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Evaluation of code quality, including strengths and areas for improvement specific to this file"
    )
    best_practices: List[str] = Field(
        description="List of adherence to or deviations from best practices in test automation or quality assurance"
    )
    complexity_assessment: str = Field(
        description="Assessment of code complexity, including qualitative evaluation"
    )
    maintainability: str = Field(
        description="Assessment of code maintainability and readability for this specific file"
    )
    recommendations: List[str] = Field(
        description="Specific recommendations for improving this file"
    )
