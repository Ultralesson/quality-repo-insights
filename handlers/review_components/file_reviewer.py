from concurrent.futures import ThreadPoolExecutor

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.language_models import LLM
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory

from handlers.models import FileReview
from handlers.prompts import FILE_REVIEW_PROMPT


class FileReviewer:
    def __init__(self, llm: LLM):
        self.__llm = llm
        self.__parser = PydanticOutputParser(pydantic_object=FileReview)

    async def review_files(self, file_items: dict[str, str], batch_size=20):
        file_reviews = {}
        file_list = list(file_items.items())

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures_to_file = {}
            for counter in range(0, len(file_list), batch_size):
                files = file_list[counter: counter + batch_size]
                for file_name, content in files:
                    future = executor.submit(self.__review_file, file_name, content)
                    futures_to_file[future] = file_name

            for future in futures_to_file:
                file_name = futures_to_file[future]
                try:
                    file_reviews[file_name] = future.result()
                except Exception as e:
                    print(f"Error reviewing {file_name}: {str(e)}")
                    file_reviews[file_name] = FileReview(overview=str(e))

        return file_reviews

    def __review_file(self, file_name: str, content: str):
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
            file_review: FileReview = chain_with_history.invoke(
                input={"input": "Kindly Provide your comprehensive review"},
                config={"configurable": {"session_id": file_name}},
            )
        except Exception as e:
            print(f"Error reviewing {file_name}: {str(e)}")
            file_review = FileReview(overview=str(e))

        return file_review
