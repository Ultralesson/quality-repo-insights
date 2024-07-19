from repository import RepositoryTraverser, JAVA_IGNORE_PATTERNS, COMMON_IGNORE_PATTERNS
from llm.hugging_face.embeddings import HuggingFaceEmbedding
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def main():
    repo_path = '/Users/sudarshan/repos/testvagrant/r3-api-automated-tests'
    ignore_patterns = [*JAVA_IGNORE_PATTERNS, *COMMON_IGNORE_PATTERNS]
    traverser = RepositoryTraverser(repo_path, HuggingFaceEmbedding())
    folder_structure = traverser.extract_folder_structure_and_contents(ignore_patterns)
    print(folder_structure)


if __name__ == '__main__':
    main()
