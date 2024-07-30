# quality-repo-insights

## About

This project leverages AI to review any code repository. It traverses the repository, generates embeddings for code files, clusters the files based on their embeddings, and then provides detailed reviews of each cluster. The reviews are summarized to produce an overall summary of the repository.

## Approach

1. **Repository Traversal**: The `RepoTraverser` class ignores files and directories specified in `ignore_patterns` and returns the folder structure with relevant details. It includes:
   - `folder_structure`: A dictionary with folders as keys and file names, chunks, and embeddings as values.
   - **Chunking & Embeddings**: Utilizes CodeBERT for generating embeddings and chunking code files.


2. **File Clustering**: Files are clustered based on their embeddings using the `FileClusterer` class.


3. **Review Generation**: Each file in a cluster is reviewed using OpenAI. Reviews are then summarized:
   - **Cluster Summary**: A summary of all files within a cluster.
   
   - **Overall Summary**: A summary of all cluster summaries, providing a high-level overview of the entire repository.

## Usage

1. **Install Dependencies**: Ensure you have Pipenv installed. Then run:
    ```bash
    pipenv install
    ```

2. **Configure Environment Variables**: Create a `.env` file in the root directory and add the following environment variables:
    ```env
    OPENAI_API_KEY=
    HUGGINGFACEHUB_API_TOKEN=
    GOOGLE_API_KEY=
    
    # Database
    SUPABASE_URL=
    SUPABASE_KEY=
    ```

3. **Run the Main Workflow**: To execute the workflow, run the main script and provide the path to the repository you want to review:
    ```bash
    pipenv run python main.py
    ```