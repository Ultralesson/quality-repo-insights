import asyncio

from dotenv import load_dotenv, find_dotenv

from handlers import UserRepoInfoHandler
from handlers.review_formatter.md_review_formatter import MDReviewFormatter
from handlers.review_handler import ReviewHandler
from handlers.review_lookup_handler import ReviewLookupHandler

load_dotenv(find_dotenv())


async def main():
    repo_info = UserRepoInfoHandler().get_repo_info()
    review_lookup_handler = ReviewLookupHandler()

    if review_lookup_handler.review_exists(repo_info.repo_path):
        overall_summary, file_reviews = ReviewLookupHandler().get_review(repo_info)
    else:
        overall_summary, file_reviews = await ReviewHandler().review_repo(repo_info)

    # Generate Output
    review_to_md = MDReviewFormatter(repo_info.name)
    await review_to_md.create_file_review_md_files(file_reviews)
    review_to_md.create_overall_summary_md_file(overall_summary)


if __name__ == "__main__":
    asyncio.run(main())
