from llm.openai.repo_summary import RepoFeedbackSummarizer
from repository import LocalRepoTraverser, JAVA_IGNORE_PATTERNS, COMMON_IGNORE_PATTERNS
from llm.embeddings.codebert_embeddings import CodeBertEmbedding
from dotenv import load_dotenv, find_dotenv
from similarity_clustering import ClusterFiles
from llm.openai.cluster_reviewer import ClusterReviewer
import asyncio

load_dotenv(find_dotenv())


async def main():
    # Traverse Repo
    repo_path = '/Users/sudarshan/repos/testvagrant/r3-api-automated-tests'
    ignore_patterns = [*JAVA_IGNORE_PATTERNS, *COMMON_IGNORE_PATTERNS]
    traverser = LocalRepoTraverser(repo_path, CodeBertEmbedding())
    folder_structure = traverser.extract_folder_structure_and_contents(ignore_patterns)

    # Cluster
    clustered_files = ClusterFiles(folder_structure).cluster_files()

    # Get Cluster Review
    reviews = await ClusterReviewer(clustered_files).review_all_clusters()

    # Final Review
    final_review = await RepoFeedbackSummarizer(reviews).summarize_feedback()
    print(final_review)


if __name__ == '__main__':
    asyncio.run(main())
