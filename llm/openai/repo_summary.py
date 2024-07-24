from random import randint
from typing import Dict, List

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatMessagePromptTemplate, \
    ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from llm.openai.parsers import CodeReviewSummary, ClusterSummary


class RepoFeedbackSummarizer:
    def __init__(
            self,
            cluster_reviews: Dict[str, Dict[str, Dict[str, CodeReviewSummary] | ClusterSummary]],
            model='gpt-4o-mini'
    ):
        self.__cluster_reviews = cluster_reviews
        self.__llm = ChatOpenAI(
            model=model,
            temperature=0.7
        )

    async def summarize_feedback(self):
        chat_history = InMemoryChatMessageHistory()
        chat_history.add_user_message("Here's the Cluster Summaries")
        for cluster, cluster_review in self.__cluster_reviews.items():
            cluster_summary = cluster_review['summary']
            if isinstance(cluster_summary, ClusterSummary):
                summary_str = (
                    f"Main Theme: {cluster_summary.main_theme}\n"
                    f"Key Points: {', '.join(cluster_summary.key_points)}\n"
                    f"Common Issues: {', '.join(cluster_summary.common_issues)}\n"
                    f"Strengths: {', '.join(cluster_summary.strengths)}\n"
                    f"Recommendations: {', '.join(cluster_summary.recommendations)}"
                )
                chat_history.add_user_message(summary_str)
            else:
                print(f"Cluster Summary not found for {cluster}")
                continue

        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                """
                You are an expert code reviewer. Provide an overall summary of the repository based on the cluster summaries.
                Focus on key points, common issues, strengths, recommendations, overall code complexity, and test coverage.
                """
            ),
            HumanMessagePromptTemplate.from_template(
                "Please summarize the cluster reviews I've provided in the chat history."
            )
        ])

        chain = chat_prompt | self.__llm | StrOutputParser()

        wrapper_chain = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=lambda _: chat_history,
            input_messages_key="input",
            history_messages_key="history"
        )

        try:
            summary = await wrapper_chain.ainvoke(
                {
                    "input": """
                                Based on the cluster summaries in the chat history, provide a comprehensive summary 
                                of the repository. Focus on identifying the key points, common issues, strengths, 
                                and recommendations. Also, comment on the overall code complexity and test coverage 
                                based on the reviews, if this information is available.
                            """
                },
                config={"configurable": {"session_id": f"{randint(0, 9999)}"}}
            )
        except Exception as e:
            summary = f"Error: {str(e)}"

        return summary
