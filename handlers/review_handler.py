from handlers.review_components import FileReviewer, ReviewSummarizer
from config import SUPABASE_URL, SUPABASE_KEY
from handlers.models import RepoInfo
from integrations.supabase import SupabaseDataClient
from llm.clients import gpt_4o_mini_llm
from repo_traverser import GitHubTraverser, LocalRepoTraverser


class ReviewHandler:

    @staticmethod
    async def review_repo(repo_info: RepoInfo, llm=gpt_4o_mini_llm()):
        traverser = (
            GitHubTraverser(repo_info.repo_path)
            if repo_info.type.lower() == "github"
            else LocalRepoTraverser(repo_info.repo_path)
        )

        # Extract Files and its contents
        files_info = await traverser.extract_contents()

        # Review Files
        files_reviews = await FileReviewer(llm).review_files(files_info)

        # Summarize reviews
        final_review = await ReviewSummarizer(llm).summarize_reviews(files_reviews)

        if SUPABASE_URL and SUPABASE_KEY:
            supabase_data_client = SupabaseDataClient()
            repo_id = supabase_data_client.add_repository(repo_info)
            await supabase_data_client.add_files_to_db(repo_id, files_reviews)
            supabase_data_client.add_overall_review_to_db(repo_id, final_review)

        return final_review, files_reviews
