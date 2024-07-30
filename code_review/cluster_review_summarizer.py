from typing import Dict

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables.history import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory

from code_review.parsers import CodeReviewSummary, ClusterSummary
from code_review.prompts.code_review_prompts import GENERAL_SUMMARIZATION_PROMPT, FORMATTED_SUMMARY_PROMPT


class ClusterReviewsSummarizer:
    def __init__(self, model='gpt-4o-mini'):
        self.__llm = ChatOpenAI(model=model, temperature=0.7)
        self.__summary_parser = PydanticOutputParser(pydantic_object=ClusterSummary)

    async def summarize_cluster(self, clusters: Dict[str, Dict[str, CodeReviewSummary]]) -> Dict[str, ClusterSummary]:
        cluster_summaries = {}
        summary_history = ChatMessageHistory()

        for cluster_id, cluster_files_reviews in clusters.items():
            for file_name, review in cluster_files_reviews.items():
                summary_history.add_user_message(
                    f"# File Name: {file_name}\n\n# Review:\n{review.to_string()}"
                )

            summarization_chain = GENERAL_SUMMARIZATION_PROMPT | self.__llm

            try:
                summary_message = await summarization_chain.ainvoke({"chat_history": summary_history.messages})
            except Exception as e:
                print(f"Error summarizing cluster reviews: {str(e)}")
                summary_message = "Error summarizing cluster reviews: {str(e)}"

            cluster_summary_chain = (
                    RunnablePassthrough.assign(
                        format_instructions=lambda _: self.__summary_parser.get_format_instructions()
                    )
                    | FORMATTED_SUMMARY_PROMPT
                    | self.__llm
                    | self.__summary_parser
            )

            try:
                cluster_summary: ClusterSummary = await cluster_summary_chain.ainvoke(
                    {"summary_message": summary_message},
                )

            except Exception as e:
                print(f"Error summarizing cluster reviews: {str(e)}")
                cluster_summary = ClusterSummary(
                    main_theme="Error occurred while summarizing this cluster",
                    key_components=[str(e)],
                    tools_and_frameworks="Error",
                    code_quality="Error",
                    best_practices="Error",
                    common_issues=["Error"],
                    maintainability="Error",
                    recommendations=["Error"],
                    complexity_assessment="Error"
                )

            cluster_summaries[cluster_id] = cluster_summary

        return cluster_summaries
