import asyncio
from collections import defaultdict

from langchain_core.chat_history import (
    InMemoryChatMessageHistory,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory

from handlers.models import FileReview
from handlers.prompts import OVERALL_SUMMARY_PROMPT


class ReviewSummarizer:

    def __init__(self, llm):
        self.__llm = llm
        self.__history = defaultdict()

    async def summarize_reviews(self, file_reviews: dict[str, FileReview]):
        futures = []
        batch_files = []

        for file_name, review in file_reviews.items():
            batch_files.append(review)

            if len(batch_files) == 10:
                future = self.__summarize_batch(batch_files)
                futures.append(future)
                batch_files = []

        if batch_files:
            futures.append(self.__summarize_batch(batch_files))

        results = await asyncio.gather(*futures)
        batch_summaries = [result for result in results]
        overall_summary = await self.__summarize_overall(batch_summaries)
        return overall_summary

    async def __summarize_batch(self, batch_files: list[FileReview]):
        history = InMemoryChatMessageHistory()
        for review in batch_files:
            if review and not review.overview.__contains__("Error reviewing"):
                history.add_user_message(review.model_dump_json())

        chain = OVERALL_SUMMARY_PROMPT | self.__llm | StrOutputParser()

        chain_with_history = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=lambda _: history,
            input_messages_key="input",
            history_messages_key="history",
        )

        try:
            summary = await chain_with_history.ainvoke(
                input={"input": "Please summarize this batch of files"},
                config={"configurable": {"session_id": "overall_batch"}},
            )
            return summary
        except Exception as e:
            raise Exception(f"Error summarizing batch: {str(e)}")

    async def __summarize_overall(self, batch_summaries: list[str]) -> str:
        summary_history = InMemoryChatMessageHistory()

        for batch_summary in batch_summaries:
            summary_history.add_user_message(f"# Batch Summary:\n{batch_summary}")

        summarization_chain = OVERALL_SUMMARY_PROMPT | self.__llm | StrOutputParser()

        chain_with_history = RunnableWithMessageHistory(
            runnable=summarization_chain,
            get_session_history=lambda _: summary_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        try:
            overall_summary = await chain_with_history.ainvoke(
                input={
                    "input": "Please summarize all file reviews into an overall review"
                },
                config={"configurable": {"session_id": "overall_final"}},
            )
            return overall_summary
        except Exception as e:
            raise Exception(f"Error summarizing overall reviews: {str(e)}")
