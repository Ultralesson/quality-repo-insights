from abc import abstractmethod
from typing import Dict


class Traverser:

    @abstractmethod
    async def extract_contents(self) -> Dict[str, str]:
        pass
