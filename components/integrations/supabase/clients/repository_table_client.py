from typing import List

from components.integrations.supabase.clients.data_repository import DataRepository
from components.integrations.supabase.models.repository import Repository


class RepositoryTableClient(DataRepository[Repository]):
    def __init__(self):
        super().__init__("repository")

    def add_repository(self, data: Repository) -> Repository:
        response = self.get_repository(data.url)
        if response is None or len(response) == 0:
            response = self._insert(
                data.model_dump(exclude_none=True, exclude_unset=True)
            )

        return response[0]

    def update_repository(self, data: Repository, repo_id: str) -> List[Repository]:
        return self._update(
            data.model_dump(exclude_unset=True, exclude_none=True), {"id": repo_id}
        )

    def get_repository(self, url: str):
        return self._select({"url": url})
