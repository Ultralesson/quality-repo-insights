from typing import Literal

from langchain_core.prompts import PromptTemplate

FILE_TYPES = Literal[
    "Test Script",
    "Object Repository",
    "Utility",
    "Configuration",
    "Setup or Teardown",
    "Reporting or Logging",
    "Framework or Library",
    "Test Data",
]

FILE_CLASSIFICATION_PROMPT = PromptTemplate.from_template(
    """
    Please classify the file into one of the following categories:
            
      1. Test Script
        - Typically contains test cases, test suites, and test data that exercise specific functionality or user flows.
        - Usually includes test logic, assertions, and verifications.
        - Can import and use elements from other categories (e.g., Element/Object Repository, Utility/Helper).
        
      2. Object Repository
        - Typically defines and stores element locators, interactions, and properties for UI, Mobile, or API elements, including API endpoints.
        - Usually contains element locators (e.g., XPath, CSS selectors, UIAutomator) and API endpoint definitions (e.g., URLs, request/response formats).
        - Typically defines element interactions (e.g., click, type, tap) and API endpoint interactions (e.g., GET, POST, PUT).
        
      3. Utility
        - Typically contains reusable functions that perform a specific task, independent of test logic.
        - Usually provides functionality for data manipulation, system interactions, or calculations.
        - Typically does not contain element locators or direct interactions with the application.
        
      4. Configuration
        - Typically stores environment-specific settings, test data, or configurations.
        - Usually contains data or settings that can be switched between environments (e.g., dev, staging, prod).
        
      5. Setup or Teardown
        - Typically contains code that runs before or after tests, including:
            - Setup and teardown code to initialize or clean up resources
            - Hooks to perform specific actions (e.g., taking screenshots)
            - Test base classes or methods that provide common functionality for tests
        - Usually includes code that is shared across multiple tests, such as:
            - Test fixtures
            - Common test data
            - Utility functions for test setup or teardown
        
      6. Reporting or Logging
        - Typically generates test reports, logs, or metrics for analysis and debugging.
        - Usually produces output for test results, logs, or metrics.
        
      7. Framework or Library
        - Typically contains custom implementations or wrappers around testing libraries or frameworks.
        - Usually provides custom functionality or extensions for testing libraries.
        
      8. Test Data 
        - Typically stores test data, input values, or expected results.
        - Usually contains data used by tests, such as input values or expected results.
        - May also include files that help generate or format test data, such as:
            - Data generators or mock data creators
            - Data transformation or mapping scripts
            - Data validation or sanitization scripts
    """
)
