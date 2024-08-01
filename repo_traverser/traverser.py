from abc import abstractmethod
from typing import Dict


class Traverser:
    @abstractmethod
    def extract_folder_structure_and_contents(self) -> Dict[str, Dict]:
        pass
