from .Display import FrameDisplay, PositionDisplay
from .Grid import Grid, RectangularGrid, Rectangle, compute_primary_grid
from .Canvas import Text, Line, compute_background_horizontal_rectangle_size, compute_background_vertical_rectangle_size
from .RectangleUtilities import compute_average, compute_rectangle_corners
from .SettingsMediator import settings_mediator
from .fire_chicken.mouse_position import MousePosition
from typing import Callable, Generator

   

class RectangularGridFrameDisplay(FrameDisplay):
    def __init__(self):
        super().__init__()
        self.grid: RectangularGrid = None

    def set_grid(self, grid: RectangularGrid): 
        primary_grid = compute_primary_grid(grid)
        super().set_grid(primary_grid)

    def set_rectangle(self, rectangle: Rectangle):
        self._perform_pre_drawing_setup_given_new_rectangle(rectangle)
        self._add_main_frame()
        if self._should_show_crisscross():
            self._add_crisscross()
    
    def _add_main_frame(self):
        frame_offset = settings_mediator.get_frame_grid_offset()
        self._add_horizontal_coordinates_to_frame(self.rectangle.top + frame_offset)
        self._add_horizontal_coordinates_to_frame(self.rectangle.bottom - frame_offset)
        self._add_vertical_coordinates_to_frame(self.rectangle.left + frame_offset)
        self._add_vertical_coordinates_to_frame(self.rectangle.right - frame_offset)

    def _add_horizontal_coordinates_to_frame(self, vertical: int):
        self._add_coordinates_to_frame(
            vertical, 
            self.grid.get_horizontal_coordinates(), 
            self.grid.compute_absolute_horizontal_from_horizontal_coordinates, 
            compute_background_horizontal_rectangle_size, 
            is_horizontal=True
        )

        
    def _add_vertical_coordinates_to_frame(self, horizontal: int):
        self._add_coordinates_to_frame(
            horizontal, 
            self.grid.get_vertical_coordinates(), 
            self.grid.compute_absolute_vertical_from_from_vertical_coordinates, 
            lambda coordinate, text_size: compute_background_vertical_rectangle_size(text_size), 
            is_horizontal=False
        )
            
    def _add_coordinates_to_frame(
            self, 
            constant_coordinate: int, 
            coordinates: Generator, 
            compute_absolute_coordinate_from_coordinate: Callable[[str], int], 
            compute_background_rectangle_size_in_dimension: Callable[[str, int], int],
            *,
            is_horizontal: bool
        ):
        is_after_first_coordinate = False
        last_absolute_coordinate = None
        too_close_threshold = None
        for coordinate in coordinates:
            absolute_coordinate = compute_absolute_coordinate_from_coordinate(coordinate)
            if is_after_first_coordinate and abs(absolute_coordinate - last_absolute_coordinate) <= too_close_threshold:
                continue
            if is_horizontal:
                horizontal = absolute_coordinate
                vertical = constant_coordinate
            else:
                horizontal = constant_coordinate
                vertical = absolute_coordinate
            text = Text(horizontal, vertical, coordinate)
            self.canvas.insert_text(text)
            last_absolute_coordinate = absolute_coordinate
            if not is_after_first_coordinate:
                is_after_first_coordinate = True
                too_close_threshold = compute_background_rectangle_size_in_dimension(coordinate, settings_mediator.get_text_size())

    def _should_show_crisscross(self) -> bool:
        return settings_mediator.get_frame_grid_should_show_crisscross()

    def _add_crisscross(self):
        self._add_vertical_lines()
        self._add_horizontal_lines()

    def _add_vertical_lines(self):
        for horizontal_coordinate in self.grid.get_horizontal_coordinates():
            horizontal = self.grid.compute_absolute_horizontal_from_horizontal_coordinates(horizontal_coordinate)
            line = Line(horizontal, self.rectangle.top, horizontal, self.rectangle.bottom)
            self.canvas.insert_line(line)
        
    def _add_horizontal_lines(self):
        for vertical_coordinate in self.grid.get_vertical_coordinates():
            vertical = self.grid.compute_absolute_vertical_from_from_vertical_coordinates(vertical_coordinate)
            line = Line(self.rectangle.left, vertical, self.rectangle.right, vertical)
            self.canvas.insert_line(line)
    
    @staticmethod
    def supports_grid(grid: Grid) -> bool:
        return is_rectangular_grid(grid)

class DoubleFrameDisplay(RectangularGridFrameDisplay):
    def set_rectangle(self, rectangle: Rectangle):
        super().set_rectangle(rectangle)
        self._add_middle_frame(rectangle)
    
    def _add_middle_frame(self, rectangle: Rectangle):
        middle_vertical = round(compute_average(rectangle.bottom, rectangle.top))
        self._add_horizontal_coordinates_to_frame(middle_vertical)
        middle_horizontal = round(compute_average(rectangle.left, rectangle.right))
        self._add_vertical_coordinates_to_frame(middle_horizontal)
    
class QuadrupleFrameDisplay(DoubleFrameDisplay):
    def set_rectangle(self, rectangle: Rectangle):
        super().set_rectangle(rectangle)
        coroners = compute_rectangle_corners(rectangle)
        for corner in coroners:
            self._add_middle_frame(corner)
        
class RectangularPositionDisplay(PositionDisplay):
    """For every horizontal and vertical coordinate combination, show the absolute position of the cursor."""
    def __init__(self):
        super().__init__()
        self.grid: RectangularGrid = None
    
    def set_grid(self, grid: RectangularGrid): 
        primary_grid = compute_primary_grid(grid)
        super().set_grid(primary_grid)
    
    def set_rectangle(self, rectangle: Rectangle):
        self._perform_pre_drawing_setup_given_new_rectangle(rectangle)
        self._add_positions()
    
    def _add_positions(self):
        last_vertical_coordinate = None
        last_horizontal_coordinate = None
        has_used_horizontal: bool = False
        for horizontal_coordinate in self.grid.get_horizontal_coordinates():
            horizontal = self.grid.compute_absolute_horizontal_from_horizontal_coordinates(horizontal_coordinate)
            has_used_horizontal = False
            for vertical_coordinate in self.grid.get_vertical_coordinates():
                vertical = self.grid.compute_absolute_vertical_from_from_vertical_coordinates(vertical_coordinate)
                position = MousePosition(horizontal, vertical)
                if self._should_include_position(last_horizontal_coordinate, last_vertical_coordinate, position):
                    self._display_text_for_position(horizontal_coordinate, vertical_coordinate, position)
                    last_vertical_coordinate = vertical_coordinate
                    has_used_horizontal = True
            if has_used_horizontal: last_horizontal_coordinate = horizontal_coordinate
            
    
    def _display_text_for_position(self, horizontal_coordinate: str, vertical_coordinate: str, position: MousePosition):
        text = Text(position.get_horizontal(), position.get_vertical(), self._compute_text_to_display(horizontal_coordinate, vertical_coordinate))
        self.canvas.insert_text(text)

    def _compute_text_to_display(self, horizontal_coordinate: str, vertical_coordinate: str) -> str:
        return vertical_coordinate + self.grid.get_coordinate_system().get_separator() + horizontal_coordinate

    def _should_include_position(self, last_horizontal_coordinate: str, last_vertical_coordinate: str, position: MousePosition) -> bool:
        if last_horizontal_coordinate is None and last_vertical_coordinate is None: return True
        if last_horizontal_coordinate is not None:
            last_horizontal = self.grid.compute_absolute_horizontal_from_horizontal_coordinates(last_horizontal_coordinate)
            if abs(position.get_horizontal() - last_horizontal) <= compute_background_horizontal_rectangle_size(self._compute_text_to_display(last_horizontal_coordinate, last_vertical_coordinate), settings_mediator.get_text_size()):
                return False
        if last_vertical_coordinate is not None:
            last_vertical = self.grid.compute_absolute_vertical_from_from_vertical_coordinates(last_vertical_coordinate)
            if abs(position.get_vertical() - last_vertical) <= compute_background_vertical_rectangle_size(settings_mediator.get_text_size()):
                return False
        return True
    
    @staticmethod
    def supports_grid(grid: Grid) -> bool:
        return is_rectangular_grid(grid)
    
def is_rectangular_grid(grid: Grid) -> bool:
    primary_grid = compute_primary_grid(grid)
    return isinstance(primary_grid, RectangularGrid)