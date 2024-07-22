from repository import RepositoryTraverser, JAVA_IGNORE_PATTERNS, COMMON_IGNORE_PATTERNS
from llm.microsoft_codebert import CodeBertEmbeddings
from dotenv import load_dotenv, find_dotenv
from similarity_clustering import ClusterFiles

load_dotenv(find_dotenv())


def main():
    repo_path = '/Users/sudarshan/repos/testvagrant/r3-api-automated-tests'
    ignore_patterns = [*JAVA_IGNORE_PATTERNS, *COMMON_IGNORE_PATTERNS]
    traverser = RepositoryTraverser(repo_path, CodeBertEmbeddings())
    folder_structure = traverser.extract_folder_structure_and_contents(ignore_patterns)
    cluster = ClusterFiles(folder_structure)
    clustered_files = cluster.cluster_files()
    cluster.print_clustered_files(clustered_files)


if __name__ == '__main__':
    main()
