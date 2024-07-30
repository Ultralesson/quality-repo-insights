import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

from langchain_openai import ChatOpenAI

from code_review.file_reviewer import FileReviewer

from langchain_core.output_parsers import PydanticOutputParser

from code_review.parsers import CodeReviewSummary
from code_review.parsers import ClusterSummary


class ClusterReviewer:
    def __init__(self, model='gpt-4o-mini'):
        self._file_reviewer = FileReviewer(model)
        self._summary_parser = PydanticOutputParser(pydantic_object=ClusterSummary)
        self.__executor = ThreadPoolExecutor()
        self._llm = ChatOpenAI(
            model=model,
            temperature=0.7
        )

    async def review_all_clusters(self, clusters: Dict[str, List[Dict[str, Dict]]]) -> Dict[
        str, Dict[str, CodeReviewSummary]]:
        cluster_reviews = {}
        tasks = []

        for cluster_name, cluster_files in clusters.items():
            for file_info in cluster_files:
                for file_name, file_content in file_info.items():
                    task = self.review_file_async(file_name, file_content['chunks'])
                    tasks.append((task, cluster_name, file_name))

        results = await asyncio.gather(*[t[0] for t in tasks])

        for result, cluster_name, file_name in zip(results, [t[1] for t in tasks], [t[2] for t in tasks]):
            if cluster_name not in cluster_reviews:
                cluster_reviews[cluster_name] = {}

            cluster_reviews[cluster_name][file_name] = result

        return cluster_reviews

    async def review_file_async(self, file_name: str, file_content: List) -> CodeReviewSummary:
        return await self._file_reviewer.review_file(file_name, file_content)
