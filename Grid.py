from .fire_chicken.mouse_position import MousePosition



class Grid:
    def __init__(self, rectangle): pass
    def compute_absolute_position(self, grid_coordinates: str) -> MousePosition: pass

class VerticallyOrderedGrid:
    def compute_absolute_position_above_grid_position_by_vertical_amount(self, grid_coordinates: str, amount: int) -> MousePosition: pass
    def compute_absolute_position_below_grid_position_by_vertical_amount(self, grid_coordinates: str, amount: int) -> MousePosition: pass

class HorizontallyOrderedGrid:
    def compute_absolute_position_to_the_right_of_grid_position_by_horizontal_amount(self, grid_coordinates: str, amount: int) -> MousePosition: pass
    def compute_absolute_position_to_the_left_of_grid_position_by_horizontal_amount(self, grid_coordinates: str, amount: int) -> MousePosition: pass