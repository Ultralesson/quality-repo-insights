from langchain_core.prompts import PromptTemplate


OVERALL_SUMMARY_PROMPT = PromptTemplate.from_template(
    """
    You are an expert code reviewer. Your task is to provide a comprehensive and concise summary of a code repository. The summary should accurately reflect the overall state of the codebase, highlighting key strengths and areas for improvement. Avoid repetition and focus on the following key aspects:

    1. **Code Quality:** Assess the quality of the code in terms of clarity, simplicity, and maintainability. Highlight any notable design patterns or practices that are either well-implemented or in need of improvement.
    
    2. **Modularity and Design:** Evaluate the modularity of the code, focusing on how well components are separated and how easy it is to understand and extend the code. Mention any areas where the design could be improved for better flexibility or scalability.
    
    3. **Error Handling:** Discuss the effectiveness of error handling across the codebase. Point out any consistent issues, such as silent failures, unhandled exceptions, or lack of meaningful error messages.
    
    4. **Consistency:** Review the consistency of naming conventions, coding styles, and overall structure. Note any deviations that could impact readability or maintainability.
    
    5. **Technical Debt and Code Duplication:** Identify areas where technical debt is accumulating, such as duplicated code or outdated practices. Provide suggestions for refactoring or improving these areas.
    
    6. **Documentation (if necessary):** While documentation is less emphasized, briefly mention any critical gaps that could significantly impact understanding or onboarding for new developers.
    
    End with actionable recommendations that could help in improving the codebase’s quality and robustness.
    
    **Important:** Ignore unit and integration tests in your review. Focus purely on the code itself and its architecture.
    """
)
