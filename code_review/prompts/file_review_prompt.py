from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

FILE_REVIEW_PROMPT = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """
        You are an expert code reviewer specializing in test automation and quality assurance. Your task is to provide a comprehensive review of code files, focusing on best practices, code quality, and effectiveness in the context of test automation. 
        
        Please structure your review according to the following format:
        {format_instructions}
        """
        ),
        HumanMessagePromptTemplate.from_template(
            """
        Please review the code segments I've provided in the chat history. The file name is {file_name}.
        
        In your review, please focus on the following aspects:
        1. The main purpose of the file in the context of test automation or quality assurance
        2. Key points or observations about the code
        3. The type of file (e.g., Test Class, Page Object, Utility, Configuration)
        4. Code quality evaluation, including strengths and areas for improvement
        5. Adherence to or deviations from best practices in test automation
        6. Assessment of code complexity
        7. Evaluation of code maintainability and readability
        8. Specific recommendations for improving the file
        
        Remember, this is a test automation project, so focus on relevant practices and patterns. 
        Don't expect to see traditional unit tests unless explicitly mentioned.
        """
        ),
        HumanMessagePromptTemplate.from_template(
            """
        Based on the code segments in the chat history, provide a comprehensive summary of the file {file_name}.
        Ensure your review covers all aspects required by the output format, including the main purpose, key points, code quality, best practices, complexity, maintainability, and specific recommendations.
        Your review should be thorough yet concise, highlighting the most important aspects of the code in the context of test automation and quality assurance.
        """
        ),
    ]
)
