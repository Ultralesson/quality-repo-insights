from typing import List


def get_formatted_li_items(list_items: List[str]):
    formatted_texts = []
    for item in list_items:
        formatted_texts.append(f"- {item}")
    return formatted_texts
