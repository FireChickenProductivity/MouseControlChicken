from .Grid import Grid
from ..RectangleUtilities import LineDivider, compute_average, Rectangle
from typing import List

class RectangularDivisionAmounts:
    def __init__(self, horizontal: int, vertical: int):
        self.horizontal = horizontal
        self.vertical = vertical

class RectangularDivisionGrid(Grid):
    def __init__(
        self, 
        division_amounts: RectangularDivisionAmounts, 
        input_coordinate_list: List[str], 
        separator: str = " "
    ):
        self.number_of_horizontal_divisions = division_amounts.horizontal
        self.number_of_vertical_divisions = division_amounts.vertical
        self.separator = separator
        self.horizontal_divider: LineDivider = None
        self.vertical_divider: LineDivider = None
        self.rectangle: Rectangle = None
    

