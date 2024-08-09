from typing import List

from pydantic import BaseModel


class JavaClassInfo(BaseModel):
    class_name: str = None
    class_modifier: str = None
    extends: str = None
    implements: List[str] = []
    fields: List[str] = []
    constructors: List[str] = []
    methods: List[str] = []
    inner_classes: List["JavaClassInfo"] = []
