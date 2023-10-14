from .fire_chicken.mouse_position import MousePosition
from typing import List

class Rectangle:
    '''Rectangle holds the coordinates of the sides of a rectangle'''
    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

class Grid:
    '''Grid is responsible for mapping from a grid coordinate system to absolute coordinates within a given rectangle on the screen'''
    def make_around(rectangle: Rectangle) -> None: pass
    def compute_absolute_position_from(self, grid_coordinates: str) -> MousePosition: pass

class VerticallyOrderedGrid:
    '''VerticallyOrderedGrid is responsible for handling a vertically ordered coordinate system'''
    def compute_absolute_position_above_grid_position_by_vertical_amount(self, grid_coordinates: str, amount: int) -> MousePosition: pass
    def compute_absolute_position_below_grid_position_by_vertical_amount(self, grid_coordinates: str, amount: int) -> MousePosition: pass
    def get_vertical_coordinates(self) -> List: pass
    def compute_absolute_vertical_from(self, coordinates) -> int: pass

class HorizontallyOrderedGrid:
    '''HorizontallyOrderedGrid is responsible for handling a horizontally ordered coordinate system'''
    def compute_absolute_position_to_the_right_of_grid_position_by_horizontal_amount(self, grid_coordinates: str, amount: int) -> MousePosition: pass
    def compute_absolute_position_to_the_left_of_grid_position_by_horizontal_amount(self, grid_coordinates: str, amount: int) -> MousePosition: pass
    def get_horizontal_coordinates(self) -> List: pass
    def compute_absolute_horizontal_from(self, coordinates) -> int: pass

class RecursiveDivisionGrid(Grid):
    '''RecursiveDivisionGrid offers a coordinate system that recursively divides a given rectangle into smaller regions such that the center of
    the region formed by a series of recursive divisions is the absolute position given by the series of coordinates causing that division'''
    def narrow_grid_using_coordinates(self, grid_coordinates: str) -> None: pass
    def compute_current_position(self) -> MousePosition: pass
    def re_expand_grid(self) -> None: pass
    def get_regions(self) -> List: pass
    def get_expansion_options(self) -> List: pass
