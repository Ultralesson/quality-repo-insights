import re

import javalang as jl
from javalang.tree import (
    ClassDeclaration,
    MethodDeclaration,
    ConstructorDeclaration,
    FieldDeclaration,
    EnumDeclaration,
    InterfaceDeclaration
)

from chunker.models import JavaFileElements, JavaClassInfo


class JavaFileChunker:

    def chunk_file(self, content: str):
        java_file_elements: JavaFileElements = JavaFileElements()
        content = self.format_java_code_with(content)

        tokens = list(jl.tokenizer.tokenize(content))
        parser = jl.parser.Parser(tokens)
        tree = parser.parse()

        java_file_elements.package = tree.package.name
        java_file_elements.imports = [f"import {file_import.path}" for file_import in tree.imports]

        types = tree.types

        for compilation_unit in types:
            if isinstance(compilation_unit, ClassDeclaration):
                class_info = self.__parse_class(tokens, content, compilation_unit)
                java_file_elements.classes.append(class_info)

            elif isinstance(compilation_unit, (EnumDeclaration, InterfaceDeclaration)):
                start_line = compilation_unit.position.line if compilation_unit.position else 0
                end_line = self.__find_end_line_using_tokens(tokens, start_line, '{', '}')
                extracted_content = self.__extract_content(content, start_line, end_line)

                if isinstance(compilation_unit, EnumDeclaration):
                    java_file_elements.enums.append(extracted_content)

                if isinstance(compilation_unit, InterfaceDeclaration):
                    java_file_elements.interfaces.append(extracted_content)

        return java_file_elements

    def __parse_class(self, tokens, content, class_declaration):
        if isinstance(class_declaration, ClassDeclaration):
            class_name = getattr(class_declaration, 'name', None)
            class_modifier_match = re.search(r"{'(.*?)'}", str(getattr(class_declaration, 'modifiers', None)))
            class_modifier = class_modifier_match.group(1) if class_modifier_match else ""
            extends_value = getattr(class_declaration, 'extends', None)
            extends = extends_value.name if extends_value else ""
            implements_attr = getattr(class_declaration, 'implements')
            implements = [implements.name for implements in implements_attr] if implements_attr else []

            constructors = []
            component_fields = []
            methods = []
            inner_classes = []

            # Process constructors
            for constructor in class_declaration.constructors:
                start_line = self.__find_start_line_with_annotations(constructor, content)
                end_line = self.__find_end_line_using_tokens(tokens, start_line, start_brace='{', end_brace='}')
                constructor_content = self.__extract_content(content, start_line, end_line)
                constructors.append(constructor_content)

            # Process fields
            for field in class_declaration.fields:
                start_line = self.__find_start_line_with_annotations(field, content)
                end_line = self.__find_end_line_using_tokens(tokens, start_line, "", ";")
                field_content = self.__extract_content(content, start_line, end_line)
                component_fields.append(field_content)

            # Process methods
            for method in class_declaration.methods:
                start_line = self.__find_start_line_with_annotations(method, content)
                end_line = self.__find_end_line_using_tokens(tokens, start_line, start_brace='{', end_brace='}')
                method_content = self.__extract_content(content, start_line, end_line)
                methods.append(method_content)

            body = getattr(class_declaration, 'body', None)
            if body:
                for item in body:
                    if isinstance(item, ClassDeclaration):
                        inner_class_info = self.__parse_class(tokens, content, item)
                        inner_classes.append(inner_class_info)

            class_info = JavaClassInfo(
                class_name=class_name,
                class_modifier=class_modifier,
                extends=extends,
                implements=implements,
                fields=component_fields,
                constructors=constructors,
                methods=methods,
                inner_classes=inner_classes
            )

            return class_info

    @staticmethod
    def __find_start_line_with_annotations(node, content):
        annotations = []
        start_pos = node.position.line

        if isinstance(node, (FieldDeclaration, MethodDeclaration, ConstructorDeclaration)):
            annotations = getattr(node, 'annotations', [])

        if annotations:
            start_pos = annotations[0].position.line - 1

            prev_line = start_pos - 1
            while prev_line >= 0:
                line_content = content.splitlines()[prev_line]
                if line_content and line_content.startswith('@'):
                    break
                elif line_content:
                    start_pos = prev_line + 1
                    break

                prev_line -= 1

        return start_pos

    @staticmethod
    def __find_end_line_using_tokens(tokens, start_line, start_brace='{', end_brace='}'):
        brace_count = 0
        end_line = start_line

        for token in tokens:
            token_line, token_value = token.position[0], token.value
            if token_line >= start_line:
                if token_value == start_brace:
                    brace_count += 1
                elif token_value == end_brace:
                    brace_count -= 1
                    if brace_count == 0:
                        end_line = token_line
                        break

        if brace_count > 0:
            end_line = max(token.position[0] for token in tokens)

        return end_line

    @staticmethod
    def __extract_content(content, start_line, end_line):
        lines = content.splitlines()
        if end_line < start_line:
            return ""
        return "\n".join(lines[start_line - 1:end_line]).strip()

    @staticmethod
    def format_java_code_with(code):
        code = code.strip()

        # Add newlines after semicolons and opening braces
        code = re.sub(r';(?!\s*$)', ';\n', code)
        code = re.sub(r'{(?!\s*$)', '{\n', code)

        # Add newlines before and after closing braces
        code = re.sub(r'(?<!\s)}', '\n}', code)
        code = re.sub(r'}(?!\s*$)', '}\n', code)

        # Indent the code
        lines = code.split('\n')
        indent = 0
        beautified_lines = []
        for line in lines:
            line = line.strip()
            if line.endswith('{'):
                beautified_lines.append('    ' * indent + line)
                indent += 1
            elif line.startswith('}'):
                indent = max(0, indent - 1)
                beautified_lines.append('    ' * indent + line)
                if not line.endswith(';'):
                    beautified_lines.append('')
            else:
                beautified_lines.append('    ' * indent + line)

        return '\n'.join(beautified_lines)
