from components.models import RepoInfo
from components.nodes.states import RepoAnalysisState
from components.traversers.traverser_factory import TraverserFactory


class RepoTraverserNode:
    def __init__(self, repo_info: RepoInfo):
        self.__traverser = TraverserFactory().create_traverser(
            repo_info.type, repo_info.repo_path
        )

    async def traverse(self, state: RepoAnalysisState):
        file_contents = await self.__traverser.extract_contents()
        state["file_contents"] = file_contents
        return state
