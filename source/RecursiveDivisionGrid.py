from .Grid import Rectangle, RecursiveDivisionGrid
from typing import List, Generator, Tuple
from .fire_chicken.mouse_position import MousePosition
from .RectangleUtilities import LineDivider, compute_average

class SquareRecursiveDivisionGrid(RecursiveDivisionGrid):
    def __init__(self, division_factor: int, separator: str = ""):
        self.division_factor: int = division_factor
        self.separator: str = separator
        self.horizontal_divider: LineDivider = None
        self.vertical_divider: LineDivider = None
        self.rectangle: Rectangle = None

    def make_around(self, rectangle: Rectangle) -> None: 
        self.rectangle = rectangle
        self.re_expand_grid()

    def compute_absolute_position_from(self, grid_coordinates: str) -> MousePosition: pass
    def narrow_grid_using_coordinates(self, grid_coordinates: str) -> None: pass
    def compute_current_position(self) -> MousePosition: 
        horizontal = compute_average(self.horizontal_divider.start, self.horizontal_divider.ending)
        vertical = compute_average(self.vertical_divider.start, self.vertical_divider.ending)
        center = MousePosition(int(horizontal), int(vertical))
        return center

    def re_expand_grid(self) -> None: 
        self.horizontal_divider = LineDivider(self.rectangle.left, self.rectangle.right, self.division_factor)
        self.vertical_divider = LineDivider(self.rectangle.top, self.rectangle.bottom, self.division_factor)
        
    def get_regions(self) -> Generator: pass

    def get_expansion_options(self) -> Generator:
        maximum_option = self.division_factor**2
        for value in range(1, maximum_option): yield str(value)
    
    def _compute_divisors_for_coordinate(self, grid_coordinate: str) -> Tuple[LineDivider, LineDivider]:
        horizontal, vertical = self._compute_grid_position_from_coordinate(grid_coordinate)
        horizontal_divider = self._compute_sub_divider(self.horizontal_divider, horizontal)
        vertical_divider = self._compute_sub_divider(self.vertical_divider, vertical)
        return horizontal_divider, vertical_divider
    
    def _compute_grid_position_from_coordinate(self, grid_coordinate: str) -> Tuple[int, int]:
        target: int = int(grid_coordinate)
        vertical: int = grid_coordinate//self.division_factor + 1
        horizontal: int = target % self.division_factor
        return horizontal, vertical

    def _compute_sub_divider(self, divisor: LineDivider, split_number: int) -> LineDivider:
        line = divisor.compute_split(split_number)
        result = LineDivider(line.start, line.ending, self.division_factor)
        return result