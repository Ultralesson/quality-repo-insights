import asyncio

from dotenv import load_dotenv, find_dotenv

from code_review.review_components import (
    ClusterSummarizer,
    RepoSummarizer,
    FileReviewer,
)
from code_review.review_formatter.review_to_md import ReviewToMd
from database.supabase import SupabaseDataClient
from user_interactions import RepoDetailsUserInteractions

load_dotenv(find_dotenv())


async def main():
    # Get User Input
    user_interactions = RepoDetailsUserInteractions()
    repo_id, traverser = user_interactions.get_repo_details()
    supabase_data_client = SupabaseDataClient(repo_id)

    # Traverse Repo
    files_info = await traverser.extract_contents()

    # Review Files
    files_reviews = await FileReviewer().review_files(files_info)

    # Create and Summarize Cluster
    clusters_summaries = await ClusterSummarizer().cluster_and_summarize(files_reviews)
    await supabase_data_client.add_cluster_and_files_to_db(clusters_summaries)

    # Final Review
    overall_summary = await RepoSummarizer().summarize_feedback(clusters_summaries)
    supabase_data_client.add_overall_review_to_db(overall_summary)

    # Generate Output
    review_to_md = ReviewToMd()
    await review_to_md.format_file_reviews(files_reviews)
    await review_to_md.format_cluster_summaries(clusters_summaries)
    review_to_md.format_overall_review(overall_summary)


if __name__ == "__main__":
    asyncio.run(main())
