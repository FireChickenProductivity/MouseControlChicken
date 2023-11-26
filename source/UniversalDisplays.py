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
        self.labeled_positions = None
    
    def set_grid(grid: Grid): pass
    def set_rectangle(rectangle: Rectangle): pass
    def show(): pass
    def hide(): pass
    def refresh(): pass