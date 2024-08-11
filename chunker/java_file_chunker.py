from tree_sitter import Node
from tree_sitter_java import language

from chunker.chunker import Chunker
from chunker.models import JavaClassInfo, JavaFileElements


class JavaFileChunker(Chunker):

    def chunk_file(self, content: str):
        if content.__contains__("class USDRatesServiceClient"):
            pass

        java_file_elements = JavaFileElements()

        parser = self._parser(language())
        tree = parser.parse(bytes(content, "utf8"))
        nodes = tree.root_node.children

        java_file_elements.package = self.__get_node_text_matching_grammar_name(
            nodes, "package_declaration"
        )
        java_file_elements.imports = self.__get_all_nodes_text(
            nodes, "import_declaration"
        )
        java_file_elements.enums = self.__get_all_nodes_text(nodes, "enum_declaration")
        java_file_elements.interfaces = self.__get_all_nodes_text(
            nodes, "interface_declaration"
        )

        class_node = self.__get_first_matching_node(nodes, "class_declaration")

        if class_node:
            java_file_elements.class_info = self.__parse_class(class_node)

        return java_file_elements.model_dump()

    def __parse_class(self, class_node: Node):
        children = class_node.children

        class_constructors = []
        class_fields = []
        class_methods = []
        inner_classes = []
        enums = []
        interfaces = []
        class_annotations = []

        class_comments = self.__get_block_comment(class_node)
        class_name = self.__get_node_text_matching_grammar_name(children, "identifier")
        class_modifier = self.__get_first_matching_node_last_child_text(
            children, "modifiers"
        )
        modifiers = self.__get_first_matching_node(children, "modifiers")
        if modifiers and len(modifiers.children) > 0:
            class_annotations = self.__get_all_nodes_text(
                modifiers.children, "annotation"
            )

        super_class = self.__get_first_matching_node_first_child_text(
            children, "superclass", "identifier"
        )

        super_interfaces = self.__get_first_matching_node_first_child_text(
            children, "super_interfaces", "type_list"
        )

        class_body = self.__get_first_matching_node(children, "class_body")
        if class_body and len(class_body.children) > 0:
            class_body_children = class_body.children
            class_constructors = self.__get_all_nodes_text(
                class_body_children, "constructor_declaration"
            )
            class_fields = self.__get_all_nodes_text(
                class_body_children, "field_declaration"
            )
            class_methods = self.__get_all_nodes_text(
                class_body_children, "method_declaration"
            )

            inner_class_nodes = self.__filter_nodes(
                class_body_children, "class_declaration"
            )

            enums = self.__get_all_nodes_text(class_body_children, "enum_declaration")

            interfaces = self.__get_all_nodes_text(
                class_body_children, "interface_declaration"
            )

            if inner_class_nodes and len(inner_class_nodes) > 0:
                for inner_class_node in inner_class_nodes:
                    inner_classes.append(self.__parse_class(inner_class_node))

        return JavaClassInfo(
            class_name=class_name,
            class_block_comments=class_comments,
            class_modifier=class_modifier,
            extends=super_class,
            implements=str(super_interfaces).split(","),
            class_annotations=class_annotations,
            fields=class_fields,
            constructors=class_constructors,
            methods=class_methods,
            inner_classes=inner_classes,
            enums=enums,
            interfaces=interfaces,
        )

    def __get_first_matching_node(
        self, nodes: list[Node], grammar_name: str
    ) -> Node | None:
        nodes = self.__filter_nodes(nodes, grammar_name)
        return nodes[0] if nodes and len(nodes) > 0 else None

    def __get_first_matching_node_first_child_text(
        self,
        nodes: list[Node],
        parent_grammar_text: str,
        child_grammar_text: str = None,
    ) -> str:
        text = ""
        node = self.__get_first_matching_node(nodes, parent_grammar_text)
        if node and len(node.children) > 0:
            if child_grammar_text is None:
                text = self.__get_node_text_with_comments(node.children[-1])
            else:
                text = self.__get_node_text_matching_grammar_name(
                    node.children, child_grammar_text
                )
        return text

    def __get_first_matching_node_last_child_text(
        self, nodes: list[Node], parent_grammar_text: str
    ) -> str:
        text = ""
        node = self.__get_first_matching_node(nodes, parent_grammar_text)
        if node and len(node.children) > 0:
            text = self.__get_node_text_with_comments(node.children[-1])
        return text

    def __get_node_text_matching_grammar_name(
        self, nodes: list[Node], grammar_name: str
    ) -> str | None:
        node = self.__get_first_matching_node(nodes, grammar_name)
        return self.__get_node_text_with_comments(node) if node else None

    def __get_all_nodes_text(self, nodes: list[Node], grammar_name: str) -> list[str]:
        matching_nodes = self.__filter_nodes(nodes, grammar_name)
        texts = []
        if matching_nodes and len(matching_nodes) > 0:
            texts = [
                self.__get_node_text_with_comments(node) for node in matching_nodes
            ]

        return texts

    def __get_node_text_with_comments(self, node: Node):
        block_comment = self.__get_block_comment(node)
        if node:
            if block_comment:
                return f"{block_comment}\n{self.__decode_bytes(node.text)}"
            else:
                return self.__decode_bytes(node.text)
        return None

    def __get_block_comment(self, node):
        if node.prev_sibling and node.prev_sibling.grammar_name == "block_comment":
            return self.__decode_bytes(node.prev_sibling.text)
        else:
            return ""

    @staticmethod
    def __filter_nodes(nodes: list[Node], grammar_name: str) -> list[Node]:
        return list(filter(lambda node: node.grammar_name == grammar_name, nodes))

    @staticmethod
    def __decode_bytes(content) -> str:
        return str(content, "utf-8")
