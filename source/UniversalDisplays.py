from .Display import FrameDisplay, PositionDisplay
from .Grid import Grid, Rectangle
from .fire_chicken.mouse_position import MousePosition
from .Canvas import Canvas, Text, Line, CanvasElementOptions

class LabeledPosition:
    def __init__(self, position: MousePosition, label: str):
        self.label = label
        self.horizontal = position.get_horizontal()
        self.vertical = position.get_vertical()
    
    def get_label(self) -> str:
        return self.label

    def get_horizontal(self) -> int:
        return self.horizontal

    def get_vertical(self) -> int:
        return self.vertical


class UniversalPositionDisplay(PositionDisplay):
    def __init__(self):
        self.grid: Grid = None
        self.canvas: Canvas = None
        self.rectangle: Rectangle = None
    
    def set_grid(self, grid: Grid): 
        self.grid = grid
        self.hide()
        if self.rectangle:
            self.set_rectangle(self.rectangle)

    def set_rectangle(self, rectangle: Rectangle):
        self.canvas = Canvas()
        self.canvas.setup(rectangle)
        self.rectangle = rectangle
        self.grid.make_around(rectangle)
        for coordinates in self.grid.get_primary_coordinates():
            position = self.grid.compute_absolute_position_from(coordinates)
            text = Text(position.get_horizontal(), position.get_vertical(), coordinates)
            self.canvas.insert_text(text)
    
from talon import ui
from .RectangularGrid import ListBasedGrid
from .RecursiveDivisionGrid import SquareRecursiveDivisionGrid
screens = ui.screens()
screen = screens[0]
talon_rectangle = screen.rect
rectangle: Rectangle = Rectangle(talon_rectangle.y, talon_rectangle.y + talon_rectangle.height, talon_rectangle.x, talon_rectangle.x + talon_rectangle.width)
# current_grid = ListBasedGrid(["a", "b", "c", "d"], ["a", "b", "c", "d", "e"])
current_grid = SquareRecursiveDivisionGrid(3)
display = UniversalPositionDisplay()
display.set_grid(current_grid)
display.set_rectangle(rectangle)
display.show()