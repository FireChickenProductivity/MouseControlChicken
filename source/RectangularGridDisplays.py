from .Display import FrameDisplay
from .Grid import Grid, RectangularGrid, Rectangle, compute_primary_grid
from .fire_chicken.mouse_position import MousePosition
from .Canvas import Canvas, Text, Line, CanvasElementOptions
from .RectangleUtilities import compute_average, compute_rectangle_corners
from .SettingsMediator import settings_mediator

class RectangularGridFrameDisplay(FrameDisplay):
    def __init__(self):
        self.grid: RectangularGrid = None
        self.canvas: Canvas = None
        self.rectangle: Rectangle = None
    
    def set_grid(self, grid: RectangularGrid): 
        self.grid = compute_primary_grid(grid)
        self.hide()
        if self.rectangle:
            self.set_rectangle(self.rectangle)

    def set_rectangle(self, rectangle: Rectangle):
        self.canvas = Canvas()
        self.canvas.setup(rectangle)
        self.rectangle = rectangle
        self.grid.make_around(rectangle)
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
