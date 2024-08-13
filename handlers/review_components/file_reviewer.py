import asyncio

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.language_models import LLM
from langchain_core.runnables.history import RunnableWithMessageHistory

from handlers.models import FileReview
from handlers.prompts import FILE_REVIEW_PROMPT


class FileReviewer:
    def __init__(self, llm: LLM):
        self.__llm = llm

    async def review_files(
        self, file_items: dict[str, str], batch_size=20
    ) -> dict[str, FileReview]:
        file_reviews = {}
        futures = []
        file_list = list(file_items.items())

        for counter in range(0, len(file_list), batch_size):
            files = file_list[counter : counter + batch_size]
            for file_name, content in files:
                future = self.__review_file(file_name, content)
                futures.append((future, file_name))

            results = await asyncio.gather(*[future[0] for future in futures])

            for file_name, review in zip([task[1] for task in futures], results):
                file_reviews[file_name] = review

            futures.clear()

        return file_reviews

    async def __review_file(self, file_name: str, content: str) -> FileReview:
        history = InMemoryChatMessageHistory()
        history.add_user_message(content)

        chain = FILE_REVIEW_PROMPT | self.__llm.with_structured_output(FileReview)

        chain_with_history = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=lambda _: history,
            input_messages_key="input",
            history_messages_key="history",
        )

        try:
            file_review: FileReview = await chain_with_history.ainvoke(
                input={"input": "Kindly Provide your comprehensive review"},
                config={"configurable": {"session_id": file_name}},
            )
        except Exception as e:
            print(f"Error reviewing {file_name}: {str(e)}")
            file_review = FileReview(overview=f"Error reviewing:\n{str(e)}")

        return file_review
