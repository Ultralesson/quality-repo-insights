from typing import List
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from code_review.parsers.code_review_summary import CodeReviewSummary
from langchain.schema.runnable import RunnablePassthrough

SYSTEM_MESSAGE_TEMPLATE = """
You are an expert code reviewer. Provide a brief summary of the code in the following format:
{format_instructions}
"""

HUMAN_MESSAGE_TEMPLATE = """
Please review the code segments i've provided in the chat history. File Name of the code segments is {file_name}.
"""

FILE_REVIEW_INPUT = """
Based on the code segments in the chat history, provide a comprehensive summary of the file.
Focus on identifying the main purpose, key points, tools usage, file name matching, and implementation details.
Don't expect Unit Tests in the code. Ensure your review covers all aspects required by the output format. 
"""


class FileReviewer:
    def __init__(self, model='gpt-4o-mini'):
        self._model = model
        self._llm = ChatOpenAI(model=model, temperature=0.7)
        self._parser = PydanticOutputParser(pydantic_object=CodeReviewSummary)

    async def review_file(self, file_name: str, chunks: List[str]) -> CodeReviewSummary:
        history = InMemoryChatMessageHistory()

        for chunk in chunks:
            history.add_user_message(chunk)

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(SYSTEM_MESSAGE_TEMPLATE),
            HumanMessagePromptTemplate.from_template(HUMAN_MESSAGE_TEMPLATE)
        ])

        chain = (
                RunnablePassthrough.assign(
                    format_instructions=lambda _: self._parser.get_format_instructions(),
                    file_name=lambda _: file_name
                )
                | prompt
                | self._llm
                | self._parser
        )

        chain_with_chat_history = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=lambda _: history,
            input_messages_key="input",
            history_messages_key="history"
        )

        try:
            file_review: CodeReviewSummary = await chain_with_chat_history.ainvoke(
                input={"input": FILE_REVIEW_INPUT},
                config={"configurable": {"session_id": file_name}}
            )

        except Exception as e:
            print(f"Error reviewing {file_name}: {str(e)}")

            file_review = CodeReviewSummary(
                main_purpose=f"Error Reviewing: {str(e)}",
                key_points="Error",
                file_type="Error",
                tools_and_libraries=[{"Error": str(e)}],
                code_quality=[{"Error": str(e)}],
                best_practices=["Error"],
                maintainability="Error",
                file_organization="Error",
                recommendations=["Error"],
                complexity_assessment=[{"Error": str(e)}]
            )

        return file_review
