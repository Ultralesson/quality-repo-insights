from typing import List

from pydantic import BaseModel


class JavaClassInfo(BaseModel):
    class_name: str = None
    class_modifier: str = None
    class_annotations: list[str] = []
    super_class: str = None
    super_interfaces: List[str] = []
    class_fields: List[str] = []
    class_constructors: List[str] = []
    class_methods: List[str] = []
    inner_classes: List["JavaClassInfo"] = []
