from typing import Dict, List

from code_review.parsers import ClusterSummary


def format_cluster_summaries(cluster_info: Dict[str, Dict]):
    for cluster_name, cluster_summaries in cluster_info.items():
        cluster_files = cluster_summaries["files"]
        cluster_summary: ClusterSummary = cluster_summaries["summary"]
        md_content = formatted_cluster_summary(cluster_summary, cluster_files)
        with open(f"review_output/cluster_reviews/{cluster_name}.md", "w") as md_file:
            md_file.write(md_content)


def __get_formatted_li_items(list_items: List[str]):
    formatted_texts = []
    for item in list_items:
        formatted_texts.append(f"- {item}")
    return formatted_texts


def formatted_cluster_summary(cluster_summary: ClusterSummary, files: List[str]):
    return f"""## Cluster Label:

{cluster_summary.cluster_name}

## Files

{'\n'.join(files)}

## Main Purpose

{cluster_summary.main_purpose}

## File Types

{'\n'.join(__get_formatted_li_items(cluster_summary.file_types))}

## Key Themes

{'\n'.join(__get_formatted_li_items(cluster_summary.key_themes))}

## Overall Code Quality

{cluster_summary.overall_code_quality}

## Best Practices Adherence

{cluster_summary.best_practices_summary}

## Complexity Evaluation

{cluster_summary.complexity_overview}

## Maintainability Overview

{cluster_summary.maintainability_assessment}

## Strengths

{'\n'.join(__get_formatted_li_items(cluster_summary.strengths))}

## Areas for Improvement

{'\n'.join(__get_formatted_li_items(cluster_summary.areas_for_improvement))}

## Recommendations

{'\n'.join(__get_formatted_li_items(cluster_summary.cluster_recommendations))}
"""
