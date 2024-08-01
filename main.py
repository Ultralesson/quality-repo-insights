import requests

from database.supabase import SupabaseDataClient
from database.supabase.models import Repository
from repo_traverser import LocalRepoTraverser, GitHubTraverser
from llm.embeddings import CodeBertEmbedder
from dotenv import load_dotenv, find_dotenv

from clustering import SimilarFilesClusterer
from code_review.review_components import ClusterReviewer, ClusterReviewsSummarizer, RepoFeedbackSummarizer
from database.supabase.clients import RepositoryTableClient
import asyncio
import os
import json

from user_interactions import RepoDetailsUserInteractions

load_dotenv(find_dotenv())


async def main():
    # Get User Input
    user_interactions = RepoDetailsUserInteractions()
    repo_type = user_interactions.get_repo_type()
    repo_name, repo_path = user_interactions.get_repo_path(repo_type)

    # Add Repo details to db
    repo_id = RepositoryTableClient().add_repository(Repository(name=repo_name, url=repo_path))
    supabase_data_client = SupabaseDataClient(repo_id)

    # Traverse Repo
    traverser = __get_traverser(repo_type, repo_path)
    folder_structure = traverser.extract_folder_structure_and_contents()

    # Cluster Files
    clustered_files = SimilarFilesClusterer().cluster_files(folder_structure)
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


def __get_traverser(repo_type, repo_path, embedder=CodeBertEmbedder()):
    if repo_type == '1':
        return GitHubTraverser(repo_path, embedder)
    return LocalRepoTraverser(repo_path, embedder)


if __name__ == '__main__':
    asyncio.run(main())
