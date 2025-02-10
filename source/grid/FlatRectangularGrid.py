from .Grid import Rectangle, RectangularGrid, FlatRectangularGrid
from .RectangularGrid import ListBasedGrid
from typing import List, Generator
from ..fire_chicken.mouse_position import MousePosition
from ..RectangleUtilities import LineDivider, compute_rectangle_from_line_splits, OneDimensionalLine

class FlatListBasedGrid(FlatRectangularGrid):
    def __init__(self, dimensions: tuple[int, int], coordinates_list: list[str], custom_coordinate_system_name="", separator: str = " "):
        size = dimensions[0] * dimensions[1]
        if len(coordinates_list) < size:
            raise ValueError("The number of coordinates is less than the number of positions on the grid")
        self.coordinates_list = coordinates_list[:size]
        vertical_num = dimensions[0]
        horizontal_num = dimensions[1]
        horizontal_coordinates_list = [str(i) for i in range(horizontal_num)]
        vertical_coordinates_list = [str(i) for i in range(vertical_num)]
        self.list_based_grid = ListBasedGrid(horizontal_coordinates_list, vertical_coordinates_list, custom_coordinate_system_name, separator)
        

    def make_around(self, rectangle: Rectangle) -> None:
        self.list_based_grid.make_around(rectangle)
    
    def compute_sub_rectangle_for(self, grid_coordinates: str) -> Rectangle:
        pass
        
    