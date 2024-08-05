from code_review.parsers import OverallSummary
from code_review.review_formatter.md_util import get_formatted_li_items


def overall_formatted_review(final_summary: OverallSummary):
    md_content = f"""## Project Overview:

{final_summary.project_overview}

## Clusters Identified

{'\n'.join(get_formatted_li_items(final_summary.main_clusters))}

## Key Strengths

{'\n'.join(get_formatted_li_items(final_summary.key_strengths))}

## Primary Concerns

{'\n'.join(get_formatted_li_items(final_summary.primary_concerns))}

## Code Quality

{final_summary.code_quality_assessment}

## Best Practices Adherence

{final_summary.best_practices_adherence}

## Complexity Evaluation

{final_summary.complexity_evaluation}

## Maintainability Overview

{final_summary.maintainability_overview}

## Patterns/Issues observed across Clusters

{'\n'.join(get_formatted_li_items(final_summary.cross_cluster_patterns))}

## Recommendations

{'\n'.join(get_formatted_li_items(final_summary.high_priority_recommendations))}

## Next Steps

{'\n'.join(get_formatted_li_items(final_summary.next_steps))}
"""
    with open("review_output/overall_summary.md", "w") as md_file:
        md_file.write(md_content)
