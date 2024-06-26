from ..InputCoordinateSystem import InputCoordinateSystem
from .Grid import Rectangle, RecursiveDivisionGrid
from typing import Generator, Tuple
from ..fire_chicken.mouse_position import MousePosition
from ..RectangleUtilities import LineDivider, compute_average, OneDimensionalLine, compute_rectangle_from_line_dividers
from ..Regions import LinearRegion, MousePositionLine
from typing import List

class RectangularDivisionAmounts:
    def __init__(self, horizontal: int, vertical: int):
        self.horizontal = horizontal
        self.vertical = vertical

class RectangularRecursiveDivisionGrid(RecursiveDivisionGrid):
    def __init__(self, division_amounts: RectangularDivisionAmounts, input_coordinate_list: List[str], separator: str = " "):
        self.horizontal_division_factor: int = division_amounts.horizontal  
        self.vertical_division_factor: int = division_amounts.vertical
        self.separator: str = separator
        self.horizontal_divider: LineDivider = None
        self.vertical_divider: LineDivider = None
        self.rectangle: Rectangle = None
        self.build_options_from_input_coordinate_list(input_coordinate_list)
        self.build_coordinate_system()

    def build_options_from_input_coordinate_list(self, input_coordinate_list: List[str]) -> None:
        self.input_coordinate_list = input_coordinate_list
        self.option_numbering = {str(index + 1): option for index, option in enumerate(input_coordinate_list)}

    def make_around(self, rectangle: Rectangle) -> None: 
        self.rectangle = rectangle
        self.reset_grid()

    def compute_absolute_position_from_valid_coordinates(self, grid_coordinates: str) -> MousePosition:
        horizontal_divider, vertical_divider = self._compute_dividers_for_coordinates(grid_coordinates)
        position = self._compute_position_from_dividers(horizontal_divider, vertical_divider)
        return position

    def narrow_grid_using_valid_coordinates(self, grid_coordinates: str) -> None:
        self.horizontal_divider, self.vertical_divider = self._compute_dividers_for_coordinates(grid_coordinates)

    def compute_sub_rectangle_for(self, grid_coordinates: str) -> Rectangle:
        subrectangle = compute_rectangle_from_line_dividers(*self._compute_dividers_for_coordinates(grid_coordinates))
        return subrectangle

    def compute_current_position(self) -> MousePosition: 
        position = self._compute_position_from_dividers(self.horizontal_divider, self.vertical_divider)
        return position
    
    def _compute_position_from_dividers(self, horizontal_divider: LineDivider, vertical_divider: LineDivider) -> MousePosition:
        horizontal = compute_average(horizontal_divider.start, horizontal_divider.ending)
        vertical = compute_average(vertical_divider.start, vertical_divider.ending)
        center = MousePosition(int(horizontal), int(vertical))
        return center

    def reset_grid(self) -> None: 
        self.horizontal_divider = LineDivider(self.rectangle.left, self.rectangle.right, self._compute_number_of_horizontal_divisions())
        self.vertical_divider = LineDivider(self.rectangle.top, self.rectangle.bottom, self._compute_number_of_vertical_divisions())
        
    def get_regions(self) -> Generator: 
        return self._get_regions_for_dividers(self.horizontal_divider, self.vertical_divider)

    def get_regions_for_sub_grid_at_coordinates(self, grid_coordinates: str) -> Generator:
        horizontal_divider, vertical_divider = self._compute_dividers_for_coordinates(grid_coordinates)
        return self._get_regions_for_dividers(horizontal_divider, vertical_divider)
            
    def _get_regions_for_dividers(self, horizontal_divider: LineDivider, vertical_divider: LineDivider) -> Generator:
        for horizontal in range(1, self.horizontal_division_factor + 1):
            horizontal_split = horizontal_divider.compute_split(horizontal)
            for vertical in range(1, self.vertical_division_factor + 1):
                vertical_split = vertical_divider.compute_split(vertical)
                region = compute_region_from_left_and_top_lines(horizontal_split, vertical_split)
                yield region

    def get_narrowing_options(self) -> Generator:
        for input_coordinate in self.option_numbering.keys(): yield input_coordinate 
    
    def _compute_dividers_for_coordinates(self, grid_coordinates: str) -> Tuple[LineDivider, LineDivider]:
        coordinates = self._compute_coordinates(grid_coordinates)
        return self._compute_dividers_for_separated_coordinates(coordinates, self.horizontal_divider, self.vertical_divider)

    def _compute_dividers_for_separated_coordinates(self, separated_coordinates: str, horizontal_divider: LineDivider, vertical_divider: LineDivider) -> Tuple[LineDivider, LineDivider]:
        horizontal_divider, vertical_divider = self._compute_dividers_for_coordinate(separated_coordinates[0], horizontal_divider, vertical_divider)
        if len(separated_coordinates) == 1: return horizontal_divider, vertical_divider
        else: return self._compute_dividers_for_separated_coordinates(separated_coordinates[1:], horizontal_divider, vertical_divider)

    def _compute_dividers_for_coordinate(self, grid_coordinate: str, horizontal_divider: LineDivider, vertical_divider: LineDivider) -> Tuple[LineDivider, LineDivider]:
        horizontal, vertical = self._compute_grid_position_from_coordinate(grid_coordinate)
        horizontal_divider = self._compute_sub_divider(horizontal_divider, horizontal, self._compute_number_of_horizontal_divisions())
        vertical_divider = self._compute_sub_divider(vertical_divider, vertical, self._compute_number_of_vertical_divisions())
        return horizontal_divider, vertical_divider
    
    def _compute_grid_position_from_coordinate(self, grid_coordinate: str) -> Tuple[int, int]:
        target: int = int(grid_coordinate)
        if target % self.horizontal_division_factor == 0: vertical = int(target/self.horizontal_division_factor)
        else: vertical = (target//self.horizontal_division_factor) + 1
        horizontal: int = (target % self.horizontal_division_factor)
        if horizontal == 0: horizontal = self.horizontal_division_factor
        return horizontal, vertical

    def _compute_sub_divider(self, divider: LineDivider, split_number: int, number_of_divisions) -> LineDivider:
        line = divider.compute_split(split_number)
        result = LineDivider(line.start, line.ending, number_of_divisions)
        return result
    
    def _compute_number_of_horizontal_divisions(self):
        return self._compute_number_of_divisions(self.horizontal_division_factor)

    def _compute_number_of_vertical_divisions(self):
        return self._compute_number_of_divisions(self.vertical_division_factor)

    def _compute_number_of_divisions(self, factor: int):
        return factor - 1

    def has_nonoverlapping_sub_rectangles(self) -> bool:
        return True

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