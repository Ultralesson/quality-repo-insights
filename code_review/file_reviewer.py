from typing import List
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from code_review.parsers.code_review_summary import CodeReviewSummary

from code_review.prompts.file_review_prompts import FILE_REVIEW_PROMPT


class FileReviewer:
    def __init__(self, model='gpt-4o-mini'):
        self._model = model
        self._llm = ChatOpenAI(model=model, temperature=0.7)
        self._parser = PydanticOutputParser(pydantic_object=CodeReviewSummary)

    async def review_file(self, file_name: str, chunks: List[str]) -> CodeReviewSummary:
        history = InMemoryChatMessageHistory()

        for chunk in chunks:
            history.add_user_message(chunk)

        chain = FILE_REVIEW_PROMPT | self._llm | self._parser

        chain_with_chat_history = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=lambda _: history,
            input_messages_key="input",
            history_messages_key="history"
        )

        try:
            file_review: CodeReviewSummary = await chain_with_chat_history.ainvoke(
                input={
                    "format_instructions": self._parser.get_format_instructions(),
                    "file_name": file_name
                },
                config={"configurable": {"session_id": file_name}}
            )

        except Exception as e:
            print(f"Error reviewing {file_name}: {str(e)}")
            file_review = CodeReviewSummary(
                main_purpose="Error occurred during review",
                key_points=["Review failed due to an error"],
                file_type="Unknown",
                code_quality={},
                best_practices=[],
                complexity_assessment="Unable to assess due to error",
                maintainability="Unable to assess due to error",
                recommendations=["Retry the review"]
            )

        return file_review
