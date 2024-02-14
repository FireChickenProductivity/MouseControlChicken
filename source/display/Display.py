from ..grid.Grid import Grid, Rectangle
from .Canvas import Canvas

DISPLAY_CLASS_NAME_POSTFIX = "Display"

class Display:
    def __init__(self):
        self.rectangle: Rectangle = None
        self.grid: Grid = None
        
    def set_grid(self, grid: Grid): 
        self.grid = grid

    def set_rectangle(self, rectangle: Rectangle): 
        self.rectangle = rectangle
    
    def draw_on(self, canvas: Canvas):
        pass
    
    @staticmethod
    def supports_grid(grid: Grid) -> bool:
        return True

    @classmethod
    def get_name(cls):
        instance = cls()
        name: str = instance.__class__.__name__[:-len(DISPLAY_CLASS_NAME_POSTFIX)]
        return name

class FrameDisplay(Display): 
    '''Displays a grid around a rectangle showing the coordinates of the grid'''
    pass

class PositionDisplay(Display):
    '''Displays a grid within a rectangle showing the positions on the grid'''
    pass