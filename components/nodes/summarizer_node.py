from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from langchain_core.language_models import BaseLanguageModel

from components.nodes.states.repo_analysis_state import RepoAnalysisState
from components.prompts import OVERALL_SUMMARY_PROMPT


class SummarizerNode:
    def __init__(self, llm: BaseLanguageModel):
        self.__summarize_chain = load_summarize_chain(
            llm,
            chain_type='refine',
            refine_prompt=OVERALL_SUMMARY_PROMPT
        )

    def summarize(self, state: RepoAnalysisState):
        reviews_docs = [
            Document(page_content=f"{filename}: {review.model_dump_json()}")
            for filename, review in state["file_reviews"].items()
        ]
        summary = self.__summarize_chain.invoke({"input_documents": reviews_docs})
        state['summary'] = summary["output_text"]
        return state

