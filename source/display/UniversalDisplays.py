from .Canvas import Canvas
from .Display import PositionDisplay
from ..Grid import Grid
from .Canvas import Text

class UniversalPositionDisplay(PositionDisplay):
    def __init__(self):
        super().__init__()
        self.grid: Grid = None

    def draw_on(self, canvas: Canvas):
        coordinate_system = self.grid.get_coordinate_system()
        for coordinates in coordinate_system.get_primary_coordinates():
            position = self.grid.compute_absolute_position_from(coordinates)
            text = Text(position.get_horizontal(), position.get_vertical(), coordinates)
            canvas.insert_text(text)