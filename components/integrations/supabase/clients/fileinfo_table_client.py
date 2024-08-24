from components.integrations.supabase.clients.data_repository import DataRepository
from components.integrations.supabase.models.file_info import FileInfo


class FileInfoTableClient(DataRepository[FileInfo]):
    def __init__(self, repo_id):
        super().__init__("file_info")
        self.__repo_id = repo_id

    def add_file_info(self, data: FileInfo):
        file_info = self.get_file_info(data.file_name)
        if len(file_info) == 0:
            return self._insert(data.model_dump(exclude_none=True, exclude_unset=True))
        else:
            return file_info

    def update_file_info(self, data: FileInfo, file_id: str):
        file_info = self.get_file_info(data.file_name, file_id)
        if len(file_info) > 0:
            return self._update(
                data=data.model_dump(exclude_none=True, exclude_unset=True),
                filter_condition={
                    "repo_id": self.__repo_id,
                    "file_name": data.file_name,
                    "id": file_id,
                },
            )
        else:
            raise Exception(f"File with id: {file_id} not found in the db")

    def get_file_info(self, file_name, file_id=None):
        filter_condition = {"file_name": file_name, "repo_id": self.__repo_id}
        if file_id is not None:
            filter_condition["id"] = file_id

        return self._select(filter_condition)

    def get_repo_files(self):
        filter_condition = {"repo_id": self.__repo_id}
        return self._select(filter_condition)
