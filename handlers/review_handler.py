from code_review.review_components import (
    FileReviewer,
)
from handlers.models import RepoInfo
from handlers.models.review import Review
from integrations.supabase import SupabaseDataClient
from integrations.supabase.clients import RepositoryTableClient
from integrations.supabase.models import Repository
from llm.clients import gpt_4o_mini_llm, ollama_llm
from repo_traverser import GitHubTraverser, LocalRepoTraverser


class ReviewHandler:

    @staticmethod
    async def review_repo(repo_info: RepoInfo) -> Review:
        repo = RepositoryTableClient().add_repository(
            Repository(
                name=repo_info.name,
                url=repo_info.repo_path,
                last_reviewed_commit=repo_info.head_commit_sha,
                branch=repo_info.branch,
            )
        )

        supabase_data_client = SupabaseDataClient(repo["id"])

        traverser = (
            GitHubTraverser(repo_info.repo_path)
            if repo_info.type.lower() == "github"
            else LocalRepoTraverser(repo_info.repo_path)
        )

        # Traverse Repo and review files
        files_info = await traverser.extract_contents()
        files_reviews = await FileReviewer(gpt_4o_mini_llm()).review_files(files_info)

        # Create and Summarize Cluster
        # clusters_reviews = await ClusterSummarizer().cluster_and_summarize(files_reviews)
        # await supabase_data_client.add_cluster_and_files_to_db(clusters_reviews)
        #
        # # Summarize Clusters and save to db
        # overall_summary = await RepoSummarizer().summarize_feedback(clusters_reviews)
        # supabase_data_client.add_overall_review_to_db(overall_summary)

        return Review(
            repo_id=repo["id"],
            overall_summary=None,
            cluster_reviews=None,
            file_reviews=files_reviews,
        )
