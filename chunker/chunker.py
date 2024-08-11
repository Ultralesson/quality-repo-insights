from abc import abstractmethod

from tree_sitter import Parser, Language


class Chunker:

    @staticmethod
    def _parser(language_int):
        parser = Parser()
        parser.language = Language(language_int)
        return parser

    @abstractmethod
    def chunk_file(self, text: str):
        pass
