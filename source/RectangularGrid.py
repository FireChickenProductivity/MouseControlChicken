from .Grid import Rectangle, RectangularGrid
from typing import List
from .fire_chicken.mouse_position import MousePosition
from .RectangleUtilities import LineDivider

class ListBasedGrid(RectangularGrid):
    '''Creates a rectangular grid with the positions corresponding to the list elements in order
        Separator is used for parsing horizontal versus vertical. Empty string separator means single character coordinates
    '''
    def __init__(self, horizontal_list: List, vertical_list: List, separator: str = ""):
        self.horizontal_list = horizontal_list
        self.vertical_list = vertical_list
        self.horizontal_coordinates = create_ordering_dictionary(horizontal_list)
        self.vertical_coordinates = create_ordering_dictionary(vertical_list)
        self.rectangle = None
        self.horizontal_divider = None
        self.vertical_divider = None
        self.separator = separator
    
    def make_around(self, rectangle: Rectangle) -> None:
        self.rectangle = rectangle
        self.horizontal_divider = LineDivider(rectangle.left, rectangle.right, len(self.horizontal_coordinates))
        self.vertical_divider = LineDivider(rectangle.top, rectangle.bottom, len(self.vertical_coordinates))
    
    def compute_absolute_position_from(self, grid_coordinates: str) -> MousePosition:
        horizontal = self.compute_absolute_horizontal_from(grid_coordinates)
        vertical = self.compute_absolute_vertical_from(grid_coordinates)
        position = MousePosition(horizontal, vertical)
        return position
    
    def get_horizontal_coordinates(self) -> List:
        return self.horizontal_list[:]

    def get_vertical_coordinates(self) -> List:
        return self.vertical_list[:]

    def compute_absolute_horizontal_from(self, coordinates: str) -> int: 
        horizontal_coordinate = self._compute_horizontal_coordinate(coordinates)
        horizontal = self.horizontal_divider.compute_divisor_position(horizontal_coordinate)
        return horizontal
    
    def compute_absolute_vertical_from(self, coordinates) -> int:
        vertical_coordinate = self._compute_vertical_coordinate(coordinates)
        vertical = self.horizontal_divider.compute_divisor_position(vertical_coordinate)
        return vertical

    def _compute_horizontal_coordinate(self, grid_coordinates: str) -> str:
        return self._compute_coordinate_from_index(grid_coordinates, 0)

    def _compute_vertical_coordinate(self, grid_coordinates: str) -> str:
        return self._compute_coordinate_from_index(grid_coordinates, 1)
    
    def _compute_coordinate_from_index(self, grid_coordinates: str, index: int) -> str:
        return self._compute_coordinates(grid_coordinates)[index]

    def _compute_coordinates(self, grid_coordinates: str) -> List:
        if len(self.separator) == 0: 
            return grid_coordinates
        else:
            return grid_coordinates.split(self.separator)

def create_ordering_dictionary(list: List):
    ordering = {}
    for index, element in list:
        ordering[element] = index + 1
    return ordering