from langchain_core.language_models import BaseLanguageModel
from langgraph.constants import END
from langgraph.graph import StateGraph

from components.models import RepoInfo
from components.nodes import (
    FileReviewerNode,
    RepoTraverserNode,
    SummarizerNode
)
from components.nodes.states import (
    RepoAnalysisState
)


class ReviewHandler:
    def __init__(self, llm: BaseLanguageModel, repo_info: RepoInfo):
        self.__llm = llm
        self.__repo_info = repo_info
        self.__graph = self.__build_graph()

    async def analyze(self) -> RepoAnalysisState:
        initial_state = {
            "repo_path": self.__repo_info.repo_path,
            "file_contents": {},
            "file_reviews": {},
            "processed_files": set(),
            "summary": "",
        }
        result = await self.__graph.ainvoke(initial_state)
        return result

    def __build_graph(self):
        traverse = RepoTraverserNode(self.__repo_info).traverse
        review = FileReviewerNode(self.__llm).review_files
        summarize = SummarizerNode(self.__llm).summarize

        graph = StateGraph(RepoAnalysisState)
        graph.add_node("traverse_repo", traverse)
        graph.add_node("review_file", review)
        graph.add_node("summarize", summarize)

        graph.add_edge("traverse_repo", "review_file")
        graph.add_conditional_edges(
            "review_file",
            self.__decide_to_continue_review_or_summarize,
            {
                "continue_review": "review_file",
                "summarize": "summarize"  #
            }
        )
        graph.add_edge("summarize", END)
        graph.set_entry_point("traverse_repo")
        return graph.compile()

    @staticmethod
    def __decide_to_continue_review_or_summarize(state: RepoAnalysisState):
        if state["file_contents"] and len(state['processed_files']) < len(state['file_contents'].keys()):
            return "continue_review"
        else:
            return "summarize"






