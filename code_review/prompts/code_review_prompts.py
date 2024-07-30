from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

GENERAL_SUMMARIZATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("placeholder, {chat_history}"),
        (
            "user",
            "Distill the above reviews into a single summary review. Include as many specific details as you can.",
        ),
    ]
)

FORMATTED_SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        """
        You are an expert code review summarizer. Format the review summary into a concise summary in the following format
        {format_instructions}
        """
    ),
    HumanMessagePromptTemplate.from_template(
        """
        # Summary Message:
        {summary_message}
        """
    )
])
