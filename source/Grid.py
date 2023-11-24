from .fire_chicken.mouse_position import MousePosition
from typing import List, Generator

class Rectangle:
    '''Rectangle holds the coordinates of the sides of a rectangle'''
    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

class Grid:
    '''Grid is responsible for mapping from a grid coordinate system to absolute coordinates within a given rectangle on the screen'''
    def make_around(self, rectangle: Rectangle) -> None: pass
    def compute_absolute_position_from(self, grid_coordinates: str) -> MousePosition: pass

class VerticallyOrderedGrid:
    '''VerticallyOrderedGrid is responsible for handling a vertically ordered coordinate system'''
    def get_vertical_coordinates(self) -> Generator: pass
    def compute_absolute_vertical_from(self, coordinates) -> int: pass

class HorizontallyOrderedGrid:
    '''HorizontallyOrderedGrid is responsible for handling a horizontally ordered coordinate system'''
    def get_horizontal_coordinates(self) -> Generator: pass
    def compute_absolute_horizontal_from(self, coordinates) -> int: pass

class RecursiveDivisionGrid(Grid):
    '''RecursiveDivisionGrid offers a coordinate system that recursively divides a given rectangle into smaller regions such that the center of
        the region formed by a series of recursive divisions is the absolute position given by the series of coordinates causing that division'''
    def narrow_grid_using_coordinates(self, grid_coordinates: str) -> None: pass
    def compute_current_position(self) -> MousePosition: pass
    def re_expand_grid(self) -> None: pass
    def get_regions(self) -> Generator: pass
    def get_expansion_options(self) -> Generator: pass

class RectangularGrid(Grid, VerticallyOrderedGrid, HorizontallyOrderedGrid):
    '''RectangularGrid offers a coordinate system that divides the given rectangle into a rectangular coordinate system such that
        the positions are determined by a vertical and a horizontal axis'''
    def get_coordinate_pairs(self) -> Generator:
        for horizontal in self.get_horizontal_coordinates():
            horizontal_value = self.compute_absolute_horizontal_from(horizontal)
            for vertical in self.get_vertical_coordinates():
                vertical_value = self.compute_absolute_vertical_from(vertical)
                yield MousePosition(horizontal_value, vertical_value)

