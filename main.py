import asyncio

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI

from components.formatters import MDOutputFormatter
from components.handlers import (
    ReviewHandler,
    ReviewLookupHandler,
    UserRepoInfoHandler
)

load_dotenv(find_dotenv())


async def main():
    repo_info = UserRepoInfoHandler().get_repo_info()
    review_lookup_handler = ReviewLookupHandler()

    if review_lookup_handler.review_exists(repo_info.repo_path):
        overall_summary, file_reviews = ReviewLookupHandler().get_review(repo_info)
    else:
        review = await ReviewHandler(
            llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.7),
            repo_info=repo_info
        ).analyze()

        overall_summary = review["summary"]
        file_reviews = review['file_reviews']

    # Generate Output
    review_to_md = MDOutputFormatter(repo_info.name)
    await review_to_md.create_file_review_md_files(file_reviews)
    review_to_md.create_overall_summary_md_file(overall_summary)


if __name__ == "__main__":
    asyncio.run(main())
