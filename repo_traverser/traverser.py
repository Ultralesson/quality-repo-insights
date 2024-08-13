from abc import abstractmethod
from typing import Dict


class Traverser:

    @abstractmethod
    def extract_contents(self) -> Dict[str, str]:
        pass
