import asyncio

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

from components.models import FileReview
from components.nodes.states import RepoAnalysisState
from components.prompts import FILE_REVIEW_PROMPT


class FileReviewerNode:
    def __init__(self, llm):
        self.__llm = llm

    async def review_files(self, state: RepoAnalysisState):
        batch_size = 20
        file_reviews = {}
        futures = []

        file_list = [{"file_name": file_name, "content": content}
                     for file_name, content in state['file_contents'].items()
                     if file_name not in state['processed_files']]

        for counter in range(0, len(file_list), batch_size):
            files = file_list[counter: counter + batch_size]
            for file in files:
                file_name = file['file_name']
                content = file['content']
                state["processed_files"] = state["processed_files"] | {file_name}
                future = self.__review_file(file_name, content)
                futures.append((future, file_name))

            results = await asyncio.gather(*[future[0] for future in futures])

            for file_name, review in zip([task[1] for task in futures], results):
                file_reviews[file_name] = review

            futures.clear()

            state['file_reviews'].update(file_reviews)
            state['processed_files'].update(file_reviews.keys())

        return state

    async def __review_file(self, file_name: str, content: str):
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
            file_review = await chain_with_history.ainvoke(
                input={"input": "Kindly Provide your comprehensive review"},
                config={"configurable": {"session_id": file_name}},
            )
        except Exception as e:
            print(f"Error reviewing {file_name}: {str(e)}")
            file_review = FileReview(overview=f"Error reviewing:\n{str(e)}")

        return file_review
