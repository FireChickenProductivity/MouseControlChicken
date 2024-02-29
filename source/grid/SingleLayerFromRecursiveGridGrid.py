from .Grid import RecursivelyDivisibleGrid, Rectangle
from ..fire_chicken.mouse_position import MousePosition

class SingleLayerFromRecursiveGridGrid(RecursivelyDivisibleGrid):
    def __init__(self, recursive_grid: RecursivelyDivisibleGrid):
        self.recursive_grid = recursive_grid
    
    def get_coordinate_system(self):
        return self.recursive_grid.get_coordinate_system().get_infinitely_repeated_system()

    def make_around(self, rectangle: Rectangle) -> None:
        return self.recursive_grid.make_around(rectangle)
    
    def compute_absolute_position_from_valid_coordinates(self, grid_coordinates: str) -> MousePosition:
        return self.recursive_grid.compute_absolute_position_from_valid_coordinates(grid_coordinates)

    def compute_sub_rectangle_for(self, grid_coordinates: str) -> Rectangle:
        return self.recursive_grid.compute_sub_rectangle_for(grid_coordinates)

    def is_combination(self) -> bool:
        return self.recursive_grid.is_combination()

    def is_wrapper(self) -> bool:
        return True

    def get_wrapped_grid(self) -> RecursivelyDivisibleGrid:
        return self.recursive_grid