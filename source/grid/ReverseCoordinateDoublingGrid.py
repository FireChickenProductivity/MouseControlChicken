from .Grid import Grid, Rectangle, CoordinatesNotSupportedException, obtain_relevant_coordinate_system_from
from ..CoordinatePrefixes import REVERSE_COORDINATES_PREFIX, obtain_coordinates_and_prefixes
from ..fire_chicken.mouse_position import MousePosition
from copy import deepcopy

class ReverseCoordinateDoublingGrid(Grid):
    def __init__(self, grid: Grid, secondary: Grid = None):
        self.primary = grid
        self.coordinate_system = obtain_relevant_coordinate_system_from(self.primary)
        if secondary:
            self.secondary = secondary
        else:
            self.secondary = deepcopy(grid)
        self.rectangle: Rectangle = None

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

    def is_wrapper(self) -> bool:
        return True

    def is_doubling(self) -> bool:
        return True
    
    def get_wrapped_grid(self) -> Grid:
        return self.get_primary_grid()
    
    def compute_absolute_position_from_reversed(self, grid_coordinates: str) -> MousePosition:
        if self.coordinate_system.do_coordinates_belong_to_system(grid_coordinates):
            return self.compute_absolute_position_from_valid_reversed_coordinates(grid_coordinates)
        raise CoordinatesNotSupportedException(grid_coordinates)
    
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

    def handle_using_coordinates_with_mouse_command(self, grid_coordinates: str) -> None:
        coordinates, prefixes = obtain_coordinates_and_prefixes(grid_coordinates)
        if REVERSE_COORDINATES_PREFIX in prefixes:
            self.secondary.handle_using_coordinates_with_mouse_command(coordinates)
        else:
            self.primary.handle_using_coordinates_with_mouse_command(coordinates)

    def compute_sub_rectangle_for(self, coordinates: str, are_coordinates_reversed: bool = False) -> Rectangle:
        if are_coordinates_reversed:
            return self.secondary.compute_sub_rectangle_for(coordinates)
        return self.primary.compute_sub_rectangle_for(coordinates)

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