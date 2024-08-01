from typing import List

from code_review.parsers import OverallSummary


def __get_formatted_li_items(list_items: List[str]):
    formatted_texts = []
    for item in list_items:
        formatted_texts.append(f"- {item}")
    return formatted_texts


def overall_formatted_review(final_summary: OverallSummary):
    md_content = f"""## Project Overview:

{final_summary.project_overview}

## Clusters Identified

{'\n'.join(__get_formatted_li_items(final_summary.main_clusters))}

## Key Strengths

{'\n'.join(__get_formatted_li_items(final_summary.key_strengths))}

## Primary Concerns

{'\n'.join(__get_formatted_li_items(final_summary.primary_concerns))}

## Code Quality

{final_summary.code_quality_assessment}

## Best Practices Adherence

{final_summary.best_practices_adherence}

## Complexity Evaluation

{final_summary.complexity_evaluation}

## Maintainability Overview

{final_summary.maintainability_overview}

## Patterns/Issues observed across Clusters

{'\n'.join(__get_formatted_li_items(final_summary.cross_cluster_patterns))}

## Recommendations

{'\n'.join(__get_formatted_li_items(final_summary.high_priority_recommendations))}

## Next Steps

{'\n'.join(__get_formatted_li_items(final_summary.next_steps))}
"""
    with open("review_output/overall_summary.md", "w") as md_file:
        md_file.write(md_content)
