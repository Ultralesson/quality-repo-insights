import asyncio
from typing import Dict, List
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from code_review.parsers import FileReview

from code_review.prompts import FILE_REVIEW_PROMPT


class CodeReviewSummary:
    pass


class FileReviewer:
    def __init__(self, model="gpt-4o-mini"):
        self._model = model
        self._llm = ChatOpenAI(model=model, temperature=0.7)
        self._parser = PydanticOutputParser(pydantic_object=FileReview)

    async def review_files(
        self, file_items: Dict[str, List], batch_size=20
    ) -> Dict[str, FileReview]:
        file_reviews: Dict[str, FileReview] = {}
        tasks = []
        file_list = list(file_items.items())

        for counter in range(0, len(file_list), batch_size):
            files = file_list[counter : counter + batch_size]
            for file_name, chunks in files:
                task = self.__review_file(file_name, chunks)
                tasks.append((task, file_name))

            results = await asyncio.gather(*[task[0] for task in tasks])

            for file_name, review in zip([task[1] for task in tasks], results):
                file_reviews[file_name] = review

            tasks.clear()

        return file_reviews

    async def __review_file(self, file_name: str, chunks: List[str]) -> FileReview:
        history = InMemoryChatMessageHistory()

        for chunk in chunks:
            history.add_user_message(chunk)

        chain = FILE_REVIEW_PROMPT | self._llm | self._parser

        chain_with_chat_history = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=lambda _: history,
            input_messages_key="input",
            history_messages_key="history",
        )

        try:
            file_review: FileReview = await chain_with_chat_history.ainvoke(
                input={
                    "format_instructions": self._parser.get_format_instructions(),
                    "file_name": file_name,
                },
                config={"configurable": {"session_id": file_name}},
            )

        except Exception as e:
            print(f"Error reviewing {file_name}: {str(e)}")
            file_review = FileReview(
                main_purpose="Error occurred during review",
                key_points=["Review failed due to an error"],
                file_type="Unknown",
                code_quality={},
                best_practices=[],
                complexity_assessment="Unable to assess due to error",
                maintainability="Unable to assess due to error",
                recommendations=["Retry the review"],
            )

        return file_review
