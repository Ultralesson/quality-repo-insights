# Quality Repo Insights

## About

This project leverages AI to review and categorize code repositories, providing valuable insights into the structure and content of test automation projects. It supports analysis of both local and GitHub repositories.

## Approach

- **Repository Traversal and Content Extraction**:
  - Traverse the repository and extract content
  - Ignore specified files and directories


-  **File Review and Summarization**:
   - Review each file and generate a summary
   - Summarize all file reviews to provide an overall summary

## Usage

1. **Install Dependencies**:
   ```bash
   pipenv install
   
2. **Configure Environment Variables**: Create a `.env` file in the root directory and add the following environment variables:
    ```env
    OPENAI_API_KEY=
    SUPABASE_URL=
    SUPABASE_KEY=
    ```
   
3. **Run the Main Workflow**: To execute the workflow, run the main script and provide the path to the repository you want to review:
    ```bash
    pipenv run python main.py
    ```