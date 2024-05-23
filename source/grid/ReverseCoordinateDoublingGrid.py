from .Grid import Grid, Rectangle, CoordinatesNotSupportedException, obtain_relevant_coordinate_system_from
from ..fire_chicken.mouse_position import MousePosition
from copy import deepcopy

class ReverseCoordinateDoublingGrid(Grid):
    def __init__(self, grid: Grid):
        self.primary = grid
        self.coordinate_system = obtain_relevant_coordinate_system_from(self.primary)
        self.secondary = deepcopy(grid)

    def make_around(self, rectangle: Rectangle) -> None:
        self.primary_rectangle = self.compute_primary_sub_rectangle_given_main_rectangle(rectangle)
        self.secondary_rectangle = self.compute_secondary_sub_rectangle_given_main_rectangle(rectangle)
        self.primary.make_around(self.primary_rectangle)
        self.secondary.make_around(self.secondary_rectangle)
        self.rectangle = rectangle
    
    def get_primary_rectangle(self) -> Rectangle:
        return self.primary_rectangle

    def get_secondary_rectangle(self) -> Rectangle:
        return self.secondary_rectangle

    def supports_reversed_coordinates(self) -> bool:
        return True
    
    def compute_absolute_position_from_reversed(self, grid_coordinates: str) -> MousePosition:
        if self.coordinate_system.do_coordinates_belong_to_system(grid_coordinates):
            return self.compute_absolute_position_from_valid_reversed_coordinates(grid_coordinates)
        raise CoordinatesNotSupportedException()
    
    def compute_absolute_position_from_valid_reversed_coordinates(self, grid_coordinates: str) -> MousePosition:
        return self.secondary.compute_absolute_position_from_valid_coordinates(grid_coordinates)

    def compute_absolute_position_from_valid_coordinates(self, grid_coordinates: str) -> MousePosition:
        return self.primary.compute_absolute_position_from_valid_coordinates(grid_coordinates)

    def compute_primary_sub_rectangle_given_main_rectangle(self, rectangle: Rectangle) -> Rectangle:
        pass

    def compute_secondary_sub_rectangle_given_main_rectangle(self, rectangle: Rectangle) -> Rectangle:
        pass

    def get_primary_grid(self) -> Grid:
        return self.primary

    def get_secondary_grid(self) -> Grid:
        return self.secondary

def compute_rectangle_length_middle(rectangle: Rectangle) -> MousePosition:
    return rectangle.left + (rectangle.right - rectangle.left) / 2

def compute_rectangle_height_middle(rectangle: Rectangle) -> MousePosition:
    return rectangle.top + (rectangle.bottom - rectangle.top) / 2
    

class ReverseCoordinateHorizontalDoublingGrid(ReverseCoordinateDoublingGrid):
    def compute_primary_sub_rectangle_given_main_rectangle(self, rectangle: Rectangle) -> Rectangle:
        return Rectangle(rectangle.top, rectangle.bottom, rectangle.left, compute_rectangle_length_middle(rectangle))

    def compute_secondary_sub_rectangle_given_main_rectangle(self, rectangle: Rectangle) -> Rectangle:
        return Rectangle(rectangle.top, rectangle.bottom, compute_rectangle_length_middle(rectangle), rectangle.right)
    
class ReverseCoordinateVerticalDoublingGrid(ReverseCoordinateDoublingGrid):
    def compute_primary_sub_rectangle_given_main_rectangle(self, rectangle: Rectangle) -> Rectangle:
        return Rectangle(rectangle.top, compute_rectangle_height_middle(rectangle), rectangle.left, rectangle.right)

    def compute_secondary_sub_rectangle_given_main_rectangle(self, rectangle: Rectangle) -> Rectangle:
        return Rectangle(compute_rectangle_height_middle(rectangle), rectangle.bottom, rectangle.left, rectangle.right)