from .Grid import Rectangle, RectangularGrid
from typing import List
from .fire_chicken import MousePosition
from .RectangleUtilities import LineDivider

class ListBasedGrid(RectangularGrid):
    '''Creates a rectangular grid with the positions corresponding to the list elements in order
        Separator is used for parsing horizontal versus vertical. Empty string separator means single character coordinates
    '''
    def __init__(self, horizontal_list: List, vertical_list: List, separator: str = ""):
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
        if len(self.separator) == 0: 
            coordinates = grid_coordinates
        else:
            coordinates = grid_coordinates.split(self.separator)
        horizontal_coordinate = coordinates[0]
        vertical_coordinate = coordinates[1]
        horizontal = self.horizontal_divider.compute_divisor_position(horizontal_coordinate)
        vertical = self.vertical_divider.compute_divisor_position(vertical_coordinate)
        position = MousePosition(horizontal, vertical)
        return position

def create_ordering_dictionary(list: List):
    ordering = {}
    for index, element in list:
        ordering[element] = index + 1
    return ordering