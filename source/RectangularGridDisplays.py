from .Display import FrameDisplay
from .Grid import Grid, RectangularGrid, Rectangle, compute_primary_grid
from .fire_chicken.mouse_position import MousePosition
from .Canvas import Canvas, Text, Line, CanvasElementOptions
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
        for horizontal_coordinate in self.grid.get_horizontal_coordinates():
            horizontal = self.grid.compute_absolute_horizontal_from_horizontal_coordinates(horizontal_coordinate)
            top_text = Text(horizontal, self.rectangle.top + frame_offset, horizontal_coordinate)
            self.canvas.insert_text(top_text)
            bottom_text = Text(horizontal, self.rectangle.bottom - frame_offset, horizontal_coordinate)
            self.canvas.insert_text(bottom_text)
        for vertical_coordinate in self.grid.get_vertical_coordinates():
            vertical = self.grid.compute_absolute_vertical_from_from_vertical_coordinates(vertical_coordinate)
            left_text = Text(self.rectangle.left + frame_offset, vertical, vertical_coordinate)
            self.canvas.insert_text(left_text)
            right_text = Text(self.rectangle.right - frame_offset, vertical, vertical_coordinate)
            self.canvas.insert_text(right_text)

    @staticmethod
    def supports_grid(grid: Grid) -> bool:
        primary_grid = compute_primary_grid(grid)
        return isinstance(primary_grid, RectangularGrid)