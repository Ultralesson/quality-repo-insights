from typing import Optional

from pydantic import BaseModel, Field


class FileReviewParser(BaseModel):
    overview: str = Field(
        description="Overview of the file's purpose and functionality."
    )
    imports_and_library_implementation: Optional[str] = Field(
        description="Feedback on the use of libraries and imports."
    )
    logic_and_implementation: Optional[str] = Field(
        description="Feedback on the logic and implementation."
    )
    best_practices_and_conventions: Optional[str] = Field(
        description="Feedback on adherence to best practices and conventions."
    )
    actionable_suggestions: Optional[str] = Field(
        description="Specific, actionable recommendations for improvement."
    )
