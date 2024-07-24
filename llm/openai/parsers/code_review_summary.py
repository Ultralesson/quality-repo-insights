from typing import List, Optional

from pydantic import BaseModel, Field


class CodeReviewSummary(BaseModel):
    main_purpose: str = Field(description="Brief description of the file's main purpose")
    key_points: List[str] = Field(description="List of key points or observations about the code")
    tool_usage: Optional[dict] = Field(
        default=None,
        description="Identification of tools or frameworks used, and assessment of their correct utilization"
    )
    implementation_details: Optional[dict] = Field(
        default=None,
        description="Evaluation of adherence to best practices and coding standards, noting any deviations or areas for improvement"
    )
    file_name_matching: str = Field(
        description="Assessment of whether the content of the file corresponds appropriately with the file name, noting any discrepancies"
    )
