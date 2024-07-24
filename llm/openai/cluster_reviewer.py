from random import randint
from typing import Dict, List

from langchain_openai import ChatOpenAI

from llm.openai.file_reviewer import FileReviewer
from langchain.memory.chat_memory import InMemoryChatMessageHistory
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory, RunnablePassthrough
from langchain_core.output_parsers import PydanticOutputParser

from llm.openai.parsers import CodeReviewSummary
from llm.openai.parsers.cluster_summary import ClusterSummary


class ClusterReviewer:
    def __init__(self, clusters: Dict[str, List[Dict[str, List[str]]]], model='gpt-4o-mini'):
        self._clusters = clusters
        self._file_reviewer = FileReviewer(model)
        self._summary_parser = PydanticOutputParser(pydantic_object=ClusterSummary)
        self._llm = ChatOpenAI(
            model=model,
            temperature=0.7
        )

    async def review_all_clusters(self) -> Dict[str, Dict[str, Dict[str, CodeReviewSummary] | ClusterSummary]]:
        all_cluster_reviews = {}
        for cluster_name, cluster_files in self._clusters.items():
            for cluster in cluster_files:
                cluster_reviews = await self.__review_cluster(cluster)
                summary = await self.__summarize_cluster(cluster_reviews)
                all_cluster_reviews[cluster_name] = {
                    'reviews': cluster_reviews,
                    'summary': summary
                }

        return all_cluster_reviews

    async def __review_cluster(self, cluster: Dict[str, List[str]]) -> Dict[str, CodeReviewSummary]:
        cluster_reviews = {}
        for file_name, chunks in cluster.items():
            file_review = await self._file_reviewer.review_file(file_name, chunks)
            cluster_reviews[file_name] = file_review

        return cluster_reviews

    async def __summarize_cluster(self, cluster_reviews: Dict[str, CodeReviewSummary]) -> ClusterSummary:
        chat_memory = InMemoryChatMessageHistory()

        for file_name, review in cluster_reviews.items():
            if isinstance(review, CodeReviewSummary):
                review_str = (
                    f"Main Purpose: {review.main_purpose}\n"
                    f"Key Points: {', '.join(review.key_points)}\n"
                    f"Tool Usage: {review.tool_usage}\n"
                    f"Implementation Details: {review.implementation_details}\n"
                    f"File Name Matching: {review.file_name_matching}\n"
                )
            else:
                print(f"Code review Summary not found for File: {file_name}")
                continue

            chat_memory.add_user_message(f"# File Name:\n{file_name}\n\n# Review:\n{review_str}")

        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                """
                You are an expert code reviewer. Summarize the following file reviews into a concise cluster summary 
                in the following format
                {format_instructions}
                """
            ),
            HumanMessagePromptTemplate.from_template(
                "Please summarize the file reviews I've provided in the chat history."
            )
        ])

        chain = (
                RunnablePassthrough.assign(
                    format_instructions=lambda _: self._summary_parser.get_format_instructions()
                )
                | chat_prompt
                | self._llm
                | self._summary_parser
        )

        wrapped_chain = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=lambda _: chat_memory,
            input_messages_key="input",
            history_messages_key="history"
        )

        try:
            cluster_summary: ClusterSummary = await wrapped_chain.ainvoke(
                {
                    "input": """
                                Based on the file reviews in the chat history, provide a comprehensive summary of this cluster. 
                                Focus on identifying the main theme, key points, common issues, strengths, and recommendations. 
                                Ensure your summary covers all aspects required by the output format. Also, comment on the overall 
                                code complexity and test coverage based on the reviews, if this information is available. 
                                Don't expect unit tests as code snippets are intended for e2e tests.
                            """
                },
                config={"configurable": {"session_id": f"{randint(0, 9999)}"}}
            )

        except Exception as e:
            print(f"Error summarizing cluster reviews: {str(e)}")
            cluster_summary = ClusterSummary(
                main_theme="Error occurred while summarizing this cluster",
                key_points=[str(e)],
                common_issues=["Review manually"],
                strengths=["Review manually"],
                recommendations=["Review manually"]
            )

        return cluster_summary
