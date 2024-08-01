from typing import Dict

from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory

from code_review.parsers.cluster_summary import ClusterSummary
from code_review.parsers.code_review_summary import CodeReviewSummary
from code_review.prompts.cluster_review_prompt import CLUSTER_FILES_SUMMARIZATION_PROMPT
import json


class ClusterReviewsSummarizer:
    def __init__(self, model='gpt-4o-mini'):
        self.__llm = ChatOpenAI(model=model, temperature=0.7)
        self.__summary_parser = PydanticOutputParser(pydantic_object=ClusterSummary)

    async def summarize_cluster(self, clusters: Dict[str, Dict[str, CodeReviewSummary]]) -> Dict[str, ClusterSummary]:
        cluster_summaries = {}
        summary_history = ChatMessageHistory()

        for cluster_id, cluster_files_reviews in clusters.items():
            for file_name, review in cluster_files_reviews.items():
                review_str = json.dumps(review.model_dump(exclude_none=True, exclude_unset=True))
                summary_history.add_user_message(
                    f"# File Name: {file_name}\n\n# Review:\n{review_str}"
                )

            summarization_chain = CLUSTER_FILES_SUMMARIZATION_PROMPT | self.__llm | self.__summary_parser

            try:
                summary: ClusterSummary = await summarization_chain.ainvoke(
                    {
                        "chat_history": summary_history.messages,
                        "format_instructions": self.__summary_parser.get_format_instructions()
                    }
                )

                cluster_summaries[cluster_id] = summary
            except Exception as e:
                raise Exception(f"Error summarizing cluster reviews: {str(e)}")

        return cluster_summaries
