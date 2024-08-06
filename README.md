# Quality Repo Insights

## About

This project uses AI to review and categorize code repositories, providing insights into the structure and content of test automation projects. It can analyze both local repositories and GitHub repositories.

## Approach

1. **Repository Traversal**: 
   - Scan through the entire repository (local or GitHub)
   - Ignore specified files and directories
   


2. **File Classification**: 
   - Use LLM to classify each file into predefined categories relevant to test automation


3. **Clustering**: 
   - Group files into clusters based on the LLM-determined categories


4. **Review and Summarization**: 
   - Generate a summary for each cluster
   - Provide an overall summary of all cluster reviews

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