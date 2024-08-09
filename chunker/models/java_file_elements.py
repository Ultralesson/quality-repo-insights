from typing import List

from pydantic import BaseModel

from chunker.models import JavaClassInfo


class JavaFileElements(BaseModel):
    package: str = None
    imports: List[str] = []
    classes: List[JavaClassInfo] = []
    enums: List[str] = []
    interfaces: List[str] = []
