from .Display import FrameDisplay, CrisscrossDisplay
from .Grid import Grid, RectangularGrid, Rectangle, compute_primary_grid
from .fire_chicken.mouse_position import MousePosition
from .Canvas import Canvas, Text, Line, CanvasElementOptions
from .RectangleUtilities import compute_average, compute_rectangle_corners
from .SettingsMediator import settings_mediator

class RectangularGridFrameDisplay(FrameDisplay):
    def __init__(self):
        super().__init__()
        self.grid: RectangularGrid = None

    def set_grid(self, grid: RectangularGrid): 
        primary_grid = compute_primary_grid(grid)
        super().set_grid(primary_grid)

    def set_rectangle(self, rectangle: Rectangle):
        self._perform_pre_drawing_setup_given_new_rectangle(rectangle)
        frame_offset = settings_mediator.get_frame_grid_offset()
        self._add_horizontal_coordinates_to_frame(self.rectangle.top + frame_offset)
        self._add_horizontal_coordinates_to_frame(self.rectangle.bottom - frame_offset)
        self._add_vertical_coordinates_to_frame(self.rectangle.left + frame_offset)
        self._add_vertical_coordinates_to_frame(self.rectangle.right - frame_offset)
    
    def _add_horizontal_coordinates_to_frame(self, vertical: int):
        for horizontal_coordinate in self.grid.get_horizontal_coordinates():
            horizontal = self.grid.compute_absolute_horizontal_from_horizontal_coordinates(horizontal_coordinate)
            text = Text(horizontal, vertical, horizontal_coordinate)
            self.canvas.insert_text(text)
        
    def _add_vertical_coordinates_to_frame(self, horizontal: int):
        for vertical_coordinate in self.grid.get_vertical_coordinates():
            vertical = self.grid.compute_absolute_vertical_from_from_vertical_coordinates(vertical_coordinate)
            text = Text(horizontal, vertical, vertical_coordinate)
            self.canvas.insert_text(text)

    @staticmethod
    def supports_grid(grid: Grid) -> bool:
        primary_grid = compute_primary_grid(grid)
        return isinstance(primary_grid, RectangularGrid)

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

class RectangularGridCrisscrossDisplay(CrisscrossDisplay):
    def __init__(self):
        super().__init__()
        self.grid: RectangularGrid = None
        self.frame_display: RectangularGridFrameDisplay = RectangularGridFrameDisplay()

    def set_grid(self, grid: RectangularGrid): 
        primary_grid = compute_primary_grid(grid)
        super().set_grid(primary_grid)
        self.frame_display.set_grid(primary_grid)

    def set_rectangle(self, rectangle: Rectangle):
        self._perform_pre_drawing_setup_given_new_rectangle(rectangle)
        self.frame_display.set_rectangle(rectangle)
        self._add_horizontal_lines()
        self._add_vertical_lines()
    
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

    def show(self):
        super().show()
        self.frame_display.show()
    
    def hide(self):
        super().hide()
        self.frame_display.hide()
    
    def refresh(self):
        super().refresh()
        self.frame_display.refresh()

    @staticmethod
    def supports_grid(grid: Grid) -> bool:
        primary_grid = compute_primary_grid(grid)
        return isinstance(primary_grid, RectangularGrid)