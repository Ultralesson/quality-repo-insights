from tree_sitter import Node
from tree_sitter_java import language

from chunker.chunker import Chunker
from chunker.models import JavaClassInfo, JavaFileElements


class JavaFileChunker(Chunker):

    def chunk_file(self, content: str):
        java_file_elements = JavaFileElements()

        parser = self._parser(language())
        tree = parser.parse(bytes(content, "utf8"))
        nodes = tree.root_node.children

        java_file_elements.package = self.__get_node_text(nodes, "package_declaration")
        java_file_elements.imports = self.__get_all_nodes_text(nodes, "import_declaration")
        java_file_elements.enums = self.__get_all_nodes_text(nodes, "enum_declaration")
        java_file_elements.interfaces = self.__get_all_nodes_text(nodes, "interface_declaration")
        java_file_elements.class_info = self.__parse_class(nodes)

        return java_file_elements

    def __parse_class(self, nodes: list[Node]):
        class_node = self.__get_first_matching_node(nodes, "class_declaration")

        if not class_node:
            return None

        children = class_node.children

        class_constructors = []
        class_fields = []
        class_methods = []

        class_name = self.__get_node_text(children, "identifier")
        class_modifier = self.__get_first_matching_node_last_child_text(children, "modifiers")
        modifiers = self.__get_first_matching_node(children, "modifiers")
        class_annotations = self.__get_all_nodes_text(modifiers.children, "annotation")
        super_class = self.__get_first_matching_node_first_child_text(
            children, "superclass", "identifier"
        )
        super_interfaces = self.__get_first_matching_node_first_child_text(
            children, "super_interfaces", "type_list"
        )
        class_body = self.__get_first_matching_node(children, "class_body")
        if class_body and len(class_body.children) > 0:
            class_body_children = class_body.children
            class_constructors = self.__get_all_nodes_text(class_body_children, "constructor_declaration")
            class_fields = self.__get_all_nodes_text(class_body_children,  "field_declaration")
            class_methods = self.__get_all_nodes_text(class_body_children, "method_declaration")

        return JavaClassInfo(
            class_name=class_name,
            class_modifier=class_modifier,
            super_class=super_class,
            super_interfaces=str(super_interfaces).split(","),
            class_annotations=class_annotations,
            class_fields=class_fields,
            class_constructors=class_constructors,
            class_methods=class_methods
        )

    def __get_node_text(self, nodes: list[Node], grammar_name: str) -> str | None:
        node = self.__get_first_matching_node(nodes, grammar_name)
        return node.text if node else None

    def __get_all_nodes_text(self, nodes: list[Node], grammar_name: str) -> list[str]:
        matching_nodes = self.__filter_nodes(nodes, grammar_name)
        texts = []
        if len(matching_nodes) > 0:
            texts = [str(node.text) for node in matching_nodes]

        return texts

    def __get_first_matching_node(self, nodes: list[Node], grammar_name: str) -> Node | None:
        nodes = self.__filter_nodes(nodes, grammar_name)
        return nodes[0] if len(nodes) > 0 else None

    def __get_first_matching_node_first_child_text(
            self,
            nodes: list[Node],
            parent_grammar_text: str,
            child_grammar_text: str = None) -> str:
        text = ""
        node = self.__get_first_matching_node(nodes, parent_grammar_text)
        if node and len(node.children) > 0:
            if child_grammar_text is None:
                text = node.children[-1].text
            else:
                text = self.__get_node_text(node.children, child_grammar_text)
        return text

    def __get_first_matching_node_last_child_text(
            self,
            nodes: list[Node],
            parent_grammar_text: str
    ) -> str:
        text = ""
        node = self.__get_first_matching_node(nodes, parent_grammar_text)
        if node and len(node.children) > 0:
            text = node.children[-1].text
        return text

    @staticmethod
    def __filter_nodes(nodes: list[Node], grammar_name: str) -> list[Node]:
        return list(filter(lambda node: node.grammar_name == grammar_name, nodes))




