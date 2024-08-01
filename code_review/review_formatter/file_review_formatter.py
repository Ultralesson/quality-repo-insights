from typing import List

from code_review.parsers import CodeReviewSummary


def __get_formatted_li_items(list_items: List[str]):
    formatted_texts = []
    for item in list_items:
        formatted_texts.append(f"- {item}")
    return formatted_texts


def formatted_file_summary(file_name: str, review_summary: CodeReviewSummary):
    md_content = f"""## Main Purpose:

{review_summary.main_purpose}

## Key Points

{'\n'.join(__get_formatted_li_items(review_summary.key_points))}

## File Type

{review_summary.file_type}

## Code Quality

{review_summary.code_quality}

## Best Practices

{'\n'.join(__get_formatted_li_items(review_summary.best_practices))}

## Complexity

{review_summary.complexity_assessment}

## Maintainability

{review_summary.maintainability}

## Recommendations

{'\n'.join(__get_formatted_li_items(review_summary.recommendations))}
"""

    with open(f"review_output/file_reviews/{file_name}.md", "w") as md_file:
        md_file.write(md_content)
