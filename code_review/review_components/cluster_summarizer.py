from typing import Dict, List

from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory

from code_review.parsers import ClusterSummary
from code_review.parsers.file_review import FileReview
from code_review.prompts.cluster_review_prompt import CLUSTER_FILES_SUMMARIZATION_PROMPT
import json

from code_review.review_components.models import ClusterInfo


class ClusterSummarizer:
    def __init__(self, model="gpt-4o-mini"):
        self.__llm = ChatOpenAI(model=model, temperature=0.7)
        self.__summary_parser = PydanticOutputParser(pydantic_object=ClusterSummary)

    async def cluster_and_summarize(
        self,
        reviews: Dict[str, FileReview],
    ) -> List[ClusterInfo]:
        cluster_summaries: List[ClusterInfo] = []
        clusters = self.__create_clusters(reviews)
        summary_history = ChatMessageHistory()

        for cluster_name, cluster_files in clusters.items():
            cluster_file_reviews: Dict[str, FileReview] = {}
            for file_name, review in cluster_files.items():
                review_str = json.dumps(
                    review.model_dump(exclude_none=True, exclude_unset=True)
                )
                cluster_file_reviews[file_name] = review
                summary_history.add_user_message(
                    f"# File Name: {file_name}\n\n# Review:\n{review_str}"
                )

            summarization_chain = (
                CLUSTER_FILES_SUMMARIZATION_PROMPT | self.__llm | self.__summary_parser
            )

            try:
                summary: ClusterSummary = await summarization_chain.ainvoke(
                    {
                        "chat_history": summary_history.messages,
                        "format_instructions": self.__summary_parser.get_format_instructions(),
                    }
                )

                cluster_summaries.append(
                    ClusterInfo(
                        name=cluster_name,
                        summary=summary,
                        file_reviews=cluster_file_reviews,
                    )
                )
            except Exception as e:
                raise Exception(f"Error summarizing cluster reviews: {str(e)}")

        return cluster_summaries

    @staticmethod
    def __create_clusters(
        file_reviews: Dict[str, FileReview],
    ) -> Dict[str, Dict[str, FileReview]]:
        clusters: Dict[str, Dict[str, FileReview]] = {}
        for file_name, review in file_reviews.items():
            file_type = review.file_type
            if file_type not in clusters:
                clusters[file_type] = {}
            clusters[file_type][file_name] = review

        return clusters
