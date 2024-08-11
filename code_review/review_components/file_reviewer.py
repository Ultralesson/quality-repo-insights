import asyncio
from collections import defaultdict

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory

from code_review.parsers.file_review_parser import FileReviewParser
from code_review.prompts import FILE_REVIEW_PROMPT


class FileReviewer:
    def __init__(self, llm):
        self.__llm = llm
        self.__files_history = defaultdict(InMemoryChatMessageHistory)
        self.__parser = PydanticOutputParser(pydantic_object=FileReviewParser)

    async def review_files(
        self, file_items: dict[str, dict], batch_size=20
    ) :
        file_reviews = {}
        tasks = []
        file_list = list(file_items.items())

        for counter in range(0, len(file_list), batch_size):
            files = file_list[counter: counter + batch_size]
            for file_name, parsed_content in files:
                task = self.__review_file(file_name, parsed_content)
                tasks.append((task, file_name))

            results = await asyncio.gather(*[task[0] for task in tasks])

            for file_name, review in zip([task[1] for task in tasks], results):
                file_reviews[file_name] = review

            tasks.clear()

        return file_reviews

    async def __review_file(self, file_name: str, parsed_content: dict):
        history = self.__get_session_history(file_name)

        def traverse(values):
            for key, value in values.items():
                if not value:
                    continue
                if isinstance(value, dict):
                    traverse(value)
                else:
                    history.add_user_message(f"{key}:\n{value}")

        for element_type, content in parsed_content.items():
            if not content:
                continue
            if isinstance(content, dict):
                traverse(content)
            else:
                history.add_user_message(f"{element_type}:\n{content}")

        chain = (
            FILE_REVIEW_PROMPT
            | self.__llm
            | self.__parser
        )

        chain_with_history = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=lambda _: history,
            input_messages_key="input",
            history_messages_key="history"
        )

        try:
            file_review = await chain_with_history.ainvoke(
                input={"input": f"Provide your review in the format {self.__parser.get_format_instructions()}"},
                config={"configurable": {"session_id": file_name}},
            )

        except Exception as e:
            print(f"Error reviewing {file_name}: {str(e)}")
            file_review = FileReviewParser(overview=str(e))

        return file_review

    def __get_session_history(self, file_name):
        if file_name not in self.__files_history:
            self.__files_history[file_name] = InMemoryChatMessageHistory()
        return self.__files_history[file_name]
