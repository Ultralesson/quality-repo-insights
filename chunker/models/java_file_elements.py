from typing import List

from pydantic import BaseModel, Field

from chunker.models import JavaClassInfo


class JavaFileElements(BaseModel):
    package: str = Field(default="")
    imports: List[str] = Field(default=[])
    class_info: JavaClassInfo = Field(default=None)
    enums: List[str] = Field(default="")
    interfaces: List[str] = Field(default="")
