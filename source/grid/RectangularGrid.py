from .Grid import Rectangle, RectangularGrid
from typing import List, Generator
from ..fire_chicken.mouse_position import MousePosition
from ..RectangleUtilities import LineDivider, compute_rectangle_from_line_splits, OneDimensionalLine, compute_average

class ListBasedGrid(RectangularGrid):
    '''Creates a rectangular grid with the positions corresponding to the list elements in order
        Separator is used for parsing horizontal versus vertical. Empty string separator means single character coordinates
    '''
    def __init__(self, horizontal_list: List, vertical_list: List, separator: str = " "):
        self.horizontal_list = horizontal_list
        self.vertical_list = vertical_list
        self.horizontal_coordinates = create_ordering_dictionary(horizontal_list)
        self.vertical_coordinates = create_ordering_dictionary(vertical_list)
        self.horizontal_divider = None
        self.vertical_divider = None
        self.separator = separator
        self.build_coordinate_system()

    @staticmethod
    def create_square_grid(coordinate_list: List, separator: str = " "):
        return ListBasedGrid(coordinate_list, coordinate_list, separator)

    def make_around(self, rectangle: Rectangle) -> None:
        self.horizontal_divider = LineDivider(rectangle.left, rectangle.right, len(self.horizontal_coordinates))
        self.vertical_divider = LineDivider(rectangle.top, rectangle.bottom, len(self.vertical_coordinates))
    
    def compute_sub_rectangle_for(self, grid_coordinates: str) -> Rectangle:
        horizontal_divider_position = self._compute_horizontal_divider_position_from(grid_coordinates)
        vertical_divider_position = self._compute_vertical_divider_position_from(grid_coordinates)
        first_horizontal_split = self.horizontal_divider.compute_split(horizontal_divider_position)
        first_vertical_split = self.vertical_divider.compute_split(vertical_divider_position)
        second_horizontal_split = self.horizontal_divider.compute_split(horizontal_divider_position + 1)
        second_vertical_split = self.vertical_divider.compute_split(vertical_divider_position + 1)
        combined_horizontal_split = OneDimensionalLine(first_horizontal_split.start, second_horizontal_split.ending)
        combined_vertical_split = OneDimensionalLine(first_vertical_split.start, second_vertical_split.ending)
        rectangle = compute_rectangle_from_line_splits(combined_horizontal_split, combined_vertical_split)
        return rectangle

    def compute_absolute_position_from_valid_coordinates(self, grid_coordinates: str) -> MousePosition:
        horizontal = self.compute_absolute_horizontal_from(grid_coordinates)
        vertical = self.compute_absolute_vertical_from(grid_coordinates)
        position = MousePosition(horizontal, vertical)
        return position
    
    def get_horizontal_coordinates(self) -> Generator:
        for element in self.horizontal_list: yield element

    def get_vertical_coordinates(self) -> Generator:
        for element in self.vertical_list: yield element

    def compute_absolute_horizontal_from(self, coordinates: str) -> int: 
        divider_position = self._compute_horizontal_divider_position_from(coordinates)
        horizontal = self.horizontal_divider.compute_divisor_position(divider_position)
        return horizontal
    
    def _compute_horizontal_divider_position_from(self, coordinates: str) -> int:
        horizontal_coordinate = self._compute_horizontal_coordinate(coordinates)
        divider_position = self.horizontal_coordinates[horizontal_coordinate]
        return divider_position

    def compute_absolute_horizontal_from_horizontal_coordinates(self, coordinates: str) -> int:
        return self.compute_absolute_horizontal_from("_" + self.separator + coordinates)
    
    def compute_absolute_vertical_from(self, coordinates: str) -> int:
        divider_position = self._compute_vertical_divider_position_from(coordinates)
        vertical = self.vertical_divider.compute_divisor_position(divider_position)
        return vertical
    
    def _compute_vertical_divider_position_from(self, coordinates: str) -> int:
        vertical_coordinate = self._compute_vertical_coordinate(coordinates)
        divider_position = self.vertical_coordinates[vertical_coordinate]
        return divider_position

    def compute_absolute_vertical_from_from_vertical_coordinates(self, coordinates: str):
        return self.compute_absolute_vertical_from(coordinates)

    def _compute_horizontal_coordinate(self, grid_coordinates: str) -> str:
        return self._compute_coordinate_from_index(grid_coordinates, 1)

    def _compute_vertical_coordinate(self, grid_coordinates: str) -> str:
        return self._compute_coordinate_from_index(grid_coordinates, 0)
    
    def _compute_coordinate_from_index(self, grid_coordinates: str, index: int) -> str:
        return self._compute_coordinates(grid_coordinates)[index]

def create_ordering_dictionary(list: List):
    ordering = {}
    for index, element in enumerate(list):
        ordering[element] = index + 1
    return ordering