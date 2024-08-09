from typing import List

from pydantic import BaseModel

from chunker.models import JavaClassInfo


class JavaFileElements(BaseModel):
    package: str = None
    imports: List[str] = []
    class_info: List[JavaClassInfo] = []
    enums: List[str] = []
    interfaces: List[str] = []
