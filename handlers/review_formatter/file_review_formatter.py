from code_review.parsers import FileReview
from handlers.review_formatter.md_util import get_formatted_li_items


def create_file_review_md(file_name: str, review_summary: FileReview, review_dir: str):
    md_content = f"""## Main Purpose:

{review_summary.main_purpose}

## Key Points

{'\n'.join(get_formatted_li_items(review_summary.key_points))}

## File Type

{review_summary.file_type}

## Code Quality

{review_summary.code_quality}

## Best Practices

{'\n'.join(get_formatted_li_items(review_summary.best_practices))}

## Complexity

{review_summary.complexity_assessment}

## Maintainability

{review_summary.maintainability}

## Recommendations

{'\n'.join(get_formatted_li_items(review_summary.recommendations))}
"""

    with open(f"{review_dir}/{file_name.replace(".", "_")}.md", "w") as md_file:
        md_file.write(md_content)
