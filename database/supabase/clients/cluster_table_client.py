from typing import List

from database.supabase.clients.data_repository import DataRepository
from database.supabase.models.cluster import Cluster


class ClusterTableClient(DataRepository[Cluster]):
    def __init__(self, repo_id: str):
        super().__init__('cluster')
        self.__repo_id = repo_id

    def add_cluster(self, data: Cluster) -> List[Cluster]:
        clusters = self.get_cluster(data.cluster_name)
        if not clusters or len(clusters) == 0:
            return self._insert(data.model_dump(exclude_none=True, exclude_unset=True))
        else:
            return [clusters]

    def update_cluster(self, data: Cluster, cluster_id: str) -> List[Cluster]:
        clusters = self._select({'id': cluster_id})
        if len(clusters) == 0:
            raise Exception(f'{cluster_id} not found')

        return self._update(data.model_dump(exclude_none=True, exclude_unset=True), {'id': cluster_id})

    def get_all_clusters(self):
        return self._select({'repo_id': self.__repo_id})

    def get_cluster(self, cluster_name: str):
        for cluster in self.get_all_clusters():
            if cluster['cluster_name'] == cluster_name:
                return cluster

        return []
