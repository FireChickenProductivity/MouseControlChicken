from .Grid import Rectangle, RecursiveDivisionGrid
from typing import Generator, Tuple
from .fire_chicken.mouse_position import MousePosition
from .RectangleUtilities import LineDivider, compute_average, OneDimensionalLine
from .Regions import LinearRegion, MousePositionLine

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

    def compute_absolute_position_from(self, grid_coordinates: str) -> MousePosition:
        horizontal_divider, vertical_divider = self._compute_dividers_for_coordinates(grid_coordinates)
        position = self._compute_position_from_dividers(horizontal_divider, vertical_divider)
        return position

    def narrow_grid_using_coordinates(self, grid_coordinates: str) -> None:
        self.horizontal_divider, self.vertical_divider = self._compute_dividers_for_coordinates(grid_coordinates)

    def compute_current_position(self) -> MousePosition: 
        position = self._compute_position_from_dividers(self.horizontal_divider, self.vertical_divider)
        return position
    
    def _compute_position_from_dividers(self, horizontal_divider: LineDivider, vertical_divider: LineDivider) -> MousePosition:
        horizontal = compute_average(horizontal_divider.start, horizontal_divider.ending)
        vertical = compute_average(vertical_divider.start, vertical_divider.ending)
        center = MousePosition(int(horizontal), int(vertical))
        return center

    def re_expand_grid(self) -> None: 
        self.horizontal_divider = LineDivider(self.rectangle.left, self.rectangle.right, self.division_factor)
        self.vertical_divider = LineDivider(self.rectangle.top, self.rectangle.bottom, self.division_factor)
        
    def get_regions(self) -> Generator: 
        for horizontal in range(1, self.division_factor):
            horizontal_split = self.horizontal_divider.compute_split(horizontal)
            for vertical in range(1, self.division_factor):
                vertical_split = self.vertical_divider.compute_split(vertical)
                region = compute_region_from_left_and_top_lines(horizontal_split, vertical_split)
                yield region

    def get_expansion_options(self) -> Generator:
        maximum_option = self.division_factor**2
        for value in range(1, maximum_option + 1): yield str(value)
    
    def _compute_dividers_for_coordinates(self, grid_coordinates: str) -> Tuple[LineDivider, LineDivider]:
        coordinates = self._compute_coordinates(grid_coordinates)
        return self._compute_dividers_for_separated_coordinates(coordinates, self.horizontal_divider, self.vertical_divider)

    def _compute_dividers_for_separated_coordinates(self, separated_coordinates: str, horizontal_divider: LineDivider, vertical_divider: LineDivider) -> Tuple[LineDivider, LineDivider]:
        horizontal_divider, vertical_divider = self._compute_dividers_for_coordinate(separated_coordinates[0], horizontal_divider, vertical_divider)
        if len(separated_coordinates) == 1: return horizontal_divider, vertical_divider
        else: return self._compute_dividers_for_separated_coordinates(separated_coordinates[1:])

    def _compute_dividers_for_coordinate(self, grid_coordinate: str, horizontal_divider: LineDivider, vertical_divider: LineDivider) -> Tuple[LineDivider, LineDivider]:
        horizontal, vertical = self._compute_grid_position_from_coordinate(grid_coordinate)
        horizontal_divider = self._compute_sub_divider(horizontal_divider, horizontal)
        vertical_divider = self._compute_sub_divider(vertical_divider, vertical)
        return horizontal_divider, vertical_divider
    
    def _compute_grid_position_from_coordinate(self, grid_coordinate: str) -> Tuple[int, int]:
        target: int = int(grid_coordinate)
        vertical: int = target//self.division_factor + 1
        horizontal: int = target % self.division_factor
        return horizontal, vertical

    def _compute_sub_divider(self, divisor: LineDivider, split_number: int) -> LineDivider:
        line = divisor.compute_split(split_number)
        result = LineDivider(line.start, line.ending, self.division_factor)
        return result

def compute_region_from_left_and_top_lines(horizontal_split: OneDimensionalLine, vertical_split: OneDimensionalLine) -> Generator:
    left = horizontal_split.start
    right = horizontal_split.ending
    top = vertical_split.start 
    bottom = vertical_split.ending
    upper_left = MousePosition(left, top)
    upper_right = MousePosition(right, top)
    bottom_left = MousePosition(left, bottom)
    bottom_right = MousePosition(right, bottom)
    lines = [MousePositionLine(upper_left, bottom_left),
             MousePositionLine(upper_left, upper_right),
             MousePositionLine(bottom_left, bottom_right),
             MousePositionLine(upper_right, bottom_right)
            ]
    region = LinearRegion(lines)
    return region