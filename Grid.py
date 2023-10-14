from .fire_chicken.mouse_position import MousePosition
from typing import List

class Rectangle:
    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

class Grid:
    def make_around(rectangle: Rectangle) -> None: pass
    def compute_absolute_position_from(self, grid_coordinates: str) -> MousePosition: pass

class VerticallyOrderedGrid:
    def compute_absolute_position_above_grid_position_by_vertical_amount(self, grid_coordinates: str, amount: int) -> MousePosition: pass
    def compute_absolute_position_below_grid_position_by_vertical_amount(self, grid_coordinates: str, amount: int) -> MousePosition: pass
    def get_vertical_coordinates(self) -> List: pass
    def compute_absolute_vertical_from(self, coordinate) -> int: pass

class HorizontallyOrderedGrid:
    def compute_absolute_position_to_the_right_of_grid_position_by_horizontal_amount(self, grid_coordinates: str, amount: int) -> MousePosition: pass
    def compute_absolute_position_to_the_left_of_grid_position_by_horizontal_amount(self, grid_coordinates: str, amount: int) -> MousePosition: pass
    def get_horizontal_coordinates(self) -> List: pass
    def compute_absolute_horizontal_from(self, coordinate) -> int: pass