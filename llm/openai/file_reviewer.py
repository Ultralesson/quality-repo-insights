from typing import List
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from llm.openai.parsers.code_review_summary import CodeReviewSummary
from langchain.schema.runnable import RunnablePassthrough

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


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
            SystemMessagePromptTemplate.from_template(
                """
                You are an expert code reviewer. Provide a brief summary of the code in the following format:
                {format_instructions}
                """
            ),
            HumanMessagePromptTemplate.from_template(
                f"File Name: {file_name}. \n Please review the code segments I've provided in the chat history."
            )
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

        wrapped_chain = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=lambda _: history,
            input_messages_key="input",
            history_messages_key="history"
        )

        try:
            file_review: CodeReviewSummary = await wrapped_chain.ainvoke(
                {
                    "input": """
                                Based on the code segments in the chat history, provide a comprehensive summary of the file. 
                                Focus on identifying the main purpose, key points, tools usage, file name matching, and 
                                implementation details. Ensure your review covers all aspects required by the output format. 
                                Don't expect Unit Tests as this is intended for e2e tests.
                                """
                },
                config={"configurable": {"session_id": file_name}}
            )

        except Exception as e:
            print(f"Error reviewing {file_name}: {str(e)}")
            file_review = CodeReviewSummary(
                main_purpose=f"Error Reviewing: {str(e)}",
                key_points="Error",
                tool_usage="Error",
                file_name_matching="Error",
                implementation_details="Error"
            )

        return file_review
