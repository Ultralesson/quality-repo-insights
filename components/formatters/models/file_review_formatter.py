import os

from components.models import FileReview


def create_file_review_md(file_name: str, review_summary: FileReview, review_dir: str):
    md_content = f"""## Overview:

{review_summary.overview}

## Imports and Library Implementations

{review_summary.imports_and_library_implementation}

## Logic and Implementation

{review_summary.logic_and_implementation}

## Best Practices and Conventions

{review_summary.best_practices_and_conventions}

## Actionable Suggestions

{review_summary.actionable_suggestions}
"""

    file = file_name.split("\\")[-1].replace(".", "_").replace(" ", "")
    file_folder = file_name.replace(file, "").replace(".", "_").replace(" ", "")
    os.makedirs(f"{review_dir}/{file_folder}", exist_ok=True)

    with open(f"{review_dir}/{file_folder}/{file}.md", "w") as md_file:
        md_file.write(md_content)
