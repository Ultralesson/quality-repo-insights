from typing import List

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from code_review.parsers import OverallSummary
from code_review.prompts import OVERALL_SUMMARY_PROMPT
import json

from code_review.review_components.models import ClusterInfo


class RepoSummarizer:
    def __init__(self, model="gpt-4o-mini"):
        self.__llm = ChatOpenAI(model=model, temperature=0.7)
        self.__parser = PydanticOutputParser(pydantic_object=OverallSummary)

    async def summarize_feedback(self, clusters: List[ClusterInfo]) -> OverallSummary:
        cluster_summaries_history = ChatMessageHistory()

        for cluster_info in clusters:
            cluster_summary = cluster_info.summary
            cluster_summaries_history.add_user_message(
                json.dumps(
                    cluster_summary.model_dump(exclude_none=True, exclude_unset=True)
                )
            )

        summarization_chain = OVERALL_SUMMARY_PROMPT | self.__llm | self.__parser

        try:
            summary: OverallSummary = await summarization_chain.ainvoke(
                input={
                    "chat_history": cluster_summaries_history.messages,
                    "format_instructions": self.__parser.get_format_instructions(),
                }
            )
        except Exception as e:
            raise Exception(f"Error summarizing cluster reviews: {str(e)}")

        return summary
