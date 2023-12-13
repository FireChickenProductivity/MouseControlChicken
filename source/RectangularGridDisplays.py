from .Display import FrameDisplay
from .Grid import RectangularGrid, Rectangle
from .fire_chicken.mouse_position import MousePosition
from .Canvas import Canvas, Text, Line, CanvasElementOptions

FRAME_OFFSET = 10

class RectangularGridFrameDisplay(FrameDisplay):
    def __init__(self):
        self.grid: RectangularGrid = None
        self.canvas: Canvas = None
        self.rectangle: Rectangle = None
    
    def set_grid(self, grid: RectangularGrid): 
        self.grid = grid
        self.hide()
        if self.rectangle:
            self.set_rectangle(self.rectangle)

    def set_rectangle(self, rectangle: Rectangle):
        self.canvas = Canvas()
        self.canvas.setup(rectangle)
        self.rectangle = rectangle
        self.grid.make_around(rectangle)
        for horizontal_coordinate in self.grid.get_horizontal_coordinates():
            horizontal = self.grid.compute_absolute_horizontal_from_horizontal_coordinates(horizontal_coordinate)
            top_text = Text(horizontal, self.rectangle.top + FRAME_OFFSET, horizontal_coordinate)
            self.canvas.insert_text(top_text)
            bottom_text = Text(horizontal, self.rectangle.bottom - FRAME_OFFSET, horizontal_coordinate)
            self.canvas.insert_text(bottom_text)
        for vertical_coordinate in self.grid.get_vertical_coordinates():
            vertical = self.grid.compute_absolute_vertical_from_from_vertical_coordinates(vertical_coordinate)
            left_text = Text(self.rectangle.left + FRAME_OFFSET, vertical, vertical_coordinate)
            self.canvas.insert_text(left_text)
            right_text = Text(self.rectangle.right - FRAME_OFFSET, vertical, vertical_coordinate)
            self.canvas.insert_text(right_text)