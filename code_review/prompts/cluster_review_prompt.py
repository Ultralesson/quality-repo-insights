from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)

CLUSTER_FILES_SUMMARIZATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are summarizing code review results for a cluster of files."
        ),
        HumanMessagePromptTemplate.from_template("{chat_history}"),
        HumanMessagePromptTemplate.from_template(
            """
        Distill the above reviews into a single summary review for this cluster.
        Please ensure that the review does not emphasize documentation-related issues or recommendations.
        Include as many specific details as you can in the following format.
        {format_instructions}
        """
        ),
    ]
)
