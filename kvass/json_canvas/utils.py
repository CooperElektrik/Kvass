from typing import Optional


def parse_color(color_str: Optional[str]) -> Optional[str]:
    if not color_str:
        return None
    return {
        "1": "red",
        "2": "orange",
        "3": "yellow",
        "4": "green",
        "5": "cyan",
        "6": "purple",
    }.get(color_str, color_str)
