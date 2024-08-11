from typing import List

from pydantic import BaseModel, Field


class JavaClassInfo(BaseModel):
    class_name: str = Field(default=None)
    class_block_comments: str = Field(default=None)
    class_modifier: str = Field(default=None)
    class_annotations: list[str] = Field(default=[])
    extends: str = Field(default=None)
    implements: List[str] = Field(default=[])
    fields: List[str] = Field(default=[])
    constructors: List[str] = Field(default=[])
    methods: List[str] = Field(default=[])
    inner_classes: List["JavaClassInfo"] = Field(default=[])
