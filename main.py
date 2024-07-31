from typing import List

import requests

from code_review.cluster_review_summarizer import ClusterReviewsSummarizer
from code_review.repo_summary import RepoFeedbackSummarizer
from database.data_clients.supabase_data_client import SupabaseDataClient
from database.supabase.models.repository import Repository
from repository import LocalRepoTraverser
from llm.embeddings.codebert_embedder import CodeBertEmbedder
from dotenv import load_dotenv, find_dotenv

from repository.github_repo_traverser import GitHubTraverser
from similarity_clustering import FileClusterer
from code_review.cluster_reviewer import ClusterReviewer
from database.supabase.clients.repository_table_client import RepositoryTableClient
import asyncio
import os
import json

load_dotenv(find_dotenv())


async def main():
    # Get User Input
    repo_type = __get_repo_type()
    repo_path = __get_repo_path(repo_type)
    repo_name = repo_path.split('/')[-1]

    # Add Repo details to db
    repo_details = RepositoryTableClient().add_repository(Repository(name=repo_name, url=repo_path))
    repo_id = repo_details[0]['id']

    supabase_data_client = SupabaseDataClient(repo_id)

    # Traverse Repo
    traverser = __get_traverser(repo_type, repo_path)
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


def __get_repo_type():
    repo_type = ''
    while repo_type == '':
        repo_type = input("Repository Type:\n1. GitHub\n2. Local\nSelect 1 or 2: ")
        if repo_type.strip() == '1' or repo_type.strip() == '2':
            return repo_type


def __get_repo_path(repo_type):
    def is_repo_type_github():
        return repo_type == '1'

    valid_repo_path = False

    while not valid_repo_path:
        repo_path = input(f'\n\nEnter the repo {'url' if is_repo_type_github() else 'path'}: ')

        if is_repo_type_github():
            valid_repo_path = requests.get(repo_path).status_code == 200
        else:
            valid_repo_path = os.path.exists(repo_path)

        if valid_repo_path:
            return repo_path


def __get_traverser(repo_type, repo_path, embedder=CodeBertEmbedder()):
    if repo_type == '1':
        return GitHubTraverser(repo_path, embedder)
    return LocalRepoTraverser(repo_path, embedder)


if __name__ == '__main__':
    asyncio.run(main())
