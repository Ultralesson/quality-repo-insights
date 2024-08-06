from typing import List, Dict

from code_review.parsers import ClusterSummary, FileReview
from code_review.review_components.models import ClusterReviewInfo
from handlers.review_formatter.md_util import get_formatted_li_items


def format_and_write_cluster_review(cluster: ClusterReviewInfo, review_dir: str):
    cluster_summary: ClusterSummary = cluster.summary
    cluster_name = cluster.name
    cluster_file_reviews: Dict[str, FileReview] = cluster.file_reviews

    cluster_files = [file_name for file_name, _ in cluster_file_reviews.items()]
    md_content = formatted_cluster_summary(cluster_summary, cluster_files)
    with open(f"{review_dir}/{cluster_name}.md", "w") as md_file:
        md_file.write(md_content)


def formatted_cluster_summary(cluster_summary: ClusterSummary, files: List[str]):
    return f"""## Files

{'\n'.join(files)}

## Main Purpose

{cluster_summary.main_purpose}

## File Types

### Primary

{cluster_summary.primary_file_type}

### Secondary

{'\n'.join(get_formatted_li_items(cluster_summary.secondary_file_types))}

## Key Themes

{'\n'.join(get_formatted_li_items(cluster_summary.key_themes))}

## Overall Code Quality

{cluster_summary.overall_code_quality}

## Best Practices Adherence

{cluster_summary.best_practices_summary}

## Complexity Evaluation

{cluster_summary.complexity_overview}

## Maintainability Overview

{cluster_summary.maintainability_assessment}

## Strengths

{'\n'.join(get_formatted_li_items(cluster_summary.strengths))}

## Areas for Improvement

{'\n'.join(get_formatted_li_items(cluster_summary.areas_for_improvement))}

## Recommendations

{'\n'.join(get_formatted_li_items(cluster_summary.cluster_recommendations))}
"""
