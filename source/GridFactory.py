from .Grid import Grid
from .RecursiveDivisionGrid import SquareRecursiveDivisionGrid
from .RectangularGrid import ListBasedGrid
from typing import List

ONE_TOO_NINE_GRID_NAME = "one to nine division"
ALPHABET_GRID_NAME = "alphabet"

ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ]

class GridFactory:
    def __init__(self):
        self.options = [ONE_TOO_NINE_GRID_NAME, ALPHABET_GRID_NAME]
    
    def get_options(self) -> List[str]:
        return self.options
    
    def create_grid(self, option: str) -> Grid:
        if option == ONE_TOO_NINE_GRID_NAME:
            return SquareRecursiveDivisionGrid(9)
        elif option == ALPHABET_GRID_NAME:
            return ListBasedGrid(ALPHABET, ALPHABET)
        