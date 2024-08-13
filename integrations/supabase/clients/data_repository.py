from typing import Dict, Any, Generic, TypeVar, List

from pydantic import BaseModel
from supabase.client import Client

from integrations.supabase.clients.supabase_client import SupabaseClient

T = TypeVar("T", bound=BaseModel)


class DataRepository(Generic[T]):
    def __init__(self, table_name: str):
        self.__client: Client = SupabaseClient()
        self.__table = self.__client.table(table_name)

    def _select(self, data: Dict[str, Any]) -> List[T]:
        try:
            response = self.__table.select("*").match(data).execute()
            return response.data
        except Exception as e:
            raise Exception(str(e))

    def _insert(self, data: Dict[str, Any]) -> List[T]:
        try:
            response = self.__table.insert(data).execute()
            return response.data
        except Exception as e:
            raise Exception(str(e))

    def _update(
        self, data: Dict[str, Any], filter_condition: Dict[str, Any]
    ) -> List[T]:
        try:
            response = self.__table.update(data).match(filter_condition).execute()
            return response.data
        except Exception as e:
            raise Exception(str(e))
