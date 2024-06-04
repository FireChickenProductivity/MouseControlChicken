from typing import List

REVERSE_COORDINATES_PREFIX = "reverse"
PREFIX_POSTFIX = ':'

def obtain_coordinates_and_prefixes(coordinates: str) -> (str, List[str]):
    if ":" in coordinates:
        prefix_text, actual_coordinates = coordinates.split(PREFIX_POSTFIX, 1)
        prefixes = prefix_text.split(",")
        return actual_coordinates, prefixes
    return coordinates, []