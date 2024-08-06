import asyncio

from dotenv import load_dotenv, find_dotenv

from handlers.md_review_formatter import MDReviewFormatter
from handlers.models.review import Review
from handlers.review_handler import ReviewHandler
from handlers import UserRepoInfoHandler
from handlers.review_lookup_handler import ReviewLookupHandler

load_dotenv(find_dotenv())


async def main():
    repo_info = UserRepoInfoHandler().get_repo_info()
    review_lookup_handler = ReviewLookupHandler()
    review: Review

    if review_lookup_handler.review_exists(repo_info.repo_path):
        review = ReviewLookupHandler().get_review(repo_info)
    else:
        review = await ReviewHandler().review_repo(repo_info)

    # # Generate Output
    review_to_md = MDReviewFormatter(review.repo_id)
    await review_to_md.create_file_review_md_files(review.file_reviews)
    await review_to_md.create_cluster_summary_md_files(review.cluster_reviews)
    review_to_md.create_overall_summary_md_file(review.overall_summary)


if __name__ == "__main__":
    asyncio.run(main())
