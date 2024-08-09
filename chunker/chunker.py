from tree_sitter import Parser, Language


class Chunker:

    @staticmethod
    def _parser(language_int):
        parser = Parser()
        parser.set_language(Language(language_int))
        return parser
