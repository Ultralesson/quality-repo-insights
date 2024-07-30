from typing import List

from database.supabase.clients.data_repository import DataRepository
from database.supabase.models.repository import Repository


class RepositoryTableClient(DataRepository[Repository]):
    def __init__(self):
        super().__init__('repository')

    def add_repository(self, data: Repository) -> List[Repository]:
        response = self.get_repository(data.url)
        if response is None or len(response) == 0:
            return self._insert(data.model_dump(exclude_none=True, exclude_unset=True))
        else:
            return response

    def update_repository(self, data: Repository, id: str) -> List[Repository]:
        return self._update(data.model_dump(exclude_unset=True, exclude_none=True), {"id": id})

    def get_repository(self, url: str):
        return self._select({"url": url})
