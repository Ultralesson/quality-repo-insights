from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
)

OVERALL_SUMMARY_PROMPT = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """
        You are creating an overall summary of a code repo_traverser based on summaries of multiple file clusters. 
        Your task is to synthesize these summaries into a comprehensive overview without referencing specific cluster names 
        or assuming knowledge about tools and frameworks that isn't explicitly mentioned in the summaries.
        """
        ),
        HumanMessagePromptTemplate.from_template(
            "Here are the summaries of different clusters in the repo_traverser:\n\n{chat_history}"
        ),
        HumanMessagePromptTemplate.from_template(
            """
        Based on these cluster summaries, provide a comprehensive overview of the entire repo_traverser. Your summary should:
        1. Provide a high-level project overview.
        2. Identify main themes and key findings across all summaries.
        3. List common issues grouped by category.
        4. Highlight overall strengths of the project.
        5. Offer priority recommendations for improvement.
        6. Briefly summarize the most significant aspects of the clusters without naming them specifically.
        7. Assess the overall complexity of the codebase.
        8. Suggest potential improvements and next steps.
        9. Identify any potential gaps in the overall testing strategy based on the file types and clusters observed.

        Do not make assumptions about specific tools or frameworks unless they are explicitly mentioned in the summaries.
        Don't expect to see traditional unit tests unless explicitly mentioned.
        Please ensure that the summary does not emphasize documentation-related issues or recommendations.

        Please structure your response according to the following format:
        {format_instructions}
        """
        ),
    ]
)
