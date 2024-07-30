from typing import Dict

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from code_review.parsers import ClusterSummary
from code_review.parsers.overall_summary import OverallSummary
from code_review.prompts.code_review_prompts import GENERAL_SUMMARIZATION_PROMPT, FORMATTED_SUMMARY_PROMPT


class RepoFeedbackSummarizer:
    def __init__(self, model='gpt-4o-mini'):
        self.__llm = ChatOpenAI(
            model=model,
            temperature=0.7
        )
        self.__parser = PydanticOutputParser(pydantic_object=OverallSummary)

    async def summarize_feedback(self, cluster_reviews: Dict[str, ClusterSummary]):
        cluster_summaries_history = ChatMessageHistory()

        for cluster, cluster_summary in cluster_reviews.items():
            cluster_summaries_history.add_user_message(cluster_summary.to_string())

        summarization_chain = GENERAL_SUMMARIZATION_PROMPT | self.__llm

        try:
            summary_message = await summarization_chain.ainvoke(
                {
                    "chat_history": cluster_summaries_history.messages
                }
            )
        except Exception as e:
            print(f"Error summarizing cluster reviews: {str(e)}")
            summary_message = "Error summarizing cluster reviews: {str(e)}"

        overall_summary_chain = (
                RunnablePassthrough.assign(
                    format_instructions=lambda _: self.__parser.get_format_instructions()
                )
                | FORMATTED_SUMMARY_PROMPT
                | self.__llm
                | self.__parser
        )

        try:
            summary: OverallSummary = await overall_summary_chain.ainvoke(
                {"summary_message": summary_message},
            )

        except Exception as e:
            print(f"Error summarizing cluster reviews: {str(e)}")
            summary = OverallSummary()

        return summary
