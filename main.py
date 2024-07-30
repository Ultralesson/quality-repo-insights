from typing import List

from code_review.cluster_review_summarizer import ClusterReviewsSummarizer
from code_review.repo_summary import RepoFeedbackSummarizer
from database.data_clients.supabase_data_client import SupabaseDataClient
from database.supabase.models.repository import Repository
from repository import LocalRepoTraverser
from llm.embeddings.codebert_embedder import CodeBertEmbedder
from dotenv import load_dotenv, find_dotenv
from similarity_clustering import FileClusterer
from code_review.cluster_reviewer import ClusterReviewer
from database.supabase.clients.repository_table_client import RepositoryTableClient
import asyncio
import os
import json

load_dotenv(find_dotenv())


async def main():
    valid_repo_path = False
    repo_details: List[Repository] = []

    while not valid_repo_path:
        repo_path = input('Enter the repo path: ')
        valid_repo_path = os.path.exists(repo_path)

        if valid_repo_path:
            repo_name = repo_path.split('/')[-1]
            repo_details = RepositoryTableClient().add_repository(Repository(name=repo_name, url=repo_path))
            break

    if len(repo_details) == 0:
        raise Exception('Repo Details not saved to db')

    repo_id = repo_details[0]['id']
    repo_url = repo_details[0]['url']
    supabase_data_client = SupabaseDataClient(repo_id)

    # Traverse Repo
    traverser = LocalRepoTraverser(repo_url, CodeBertEmbedder())
    folder_structure = traverser.extract_folder_structure_and_contents()

    # Cluster
    clustered_files = FileClusterer().cluster_files(folder_structure)
    supabase_data_client.add_clusters_and_files_to_db(clustered_files)

    # Get Cluster Review
    cluster_file_reviews = await ClusterReviewer().review_all_clusters(clustered_files)
    supabase_data_client.add_file_reviews_to_db(cluster_file_reviews)

    # Summarize Cluster Reviews
    clusters_summaries = await ClusterReviewsSummarizer().summarize_cluster(cluster_file_reviews)
    supabase_data_client.add_cluster_summary_to_db(clusters_summaries)

    # Final Review
    final_review = await RepoFeedbackSummarizer().summarize_feedback(clusters_summaries)
    supabase_data_client.add_overall_review_to_db(final_review)
    print('Final Review:\n\n')
    print(json.dumps(final_review.model_dump(exclude_none=True, exclude_unset=True)))


if __name__ == '__main__':
    asyncio.run(main())
