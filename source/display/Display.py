from ..grid.Grid import Grid, Rectangle
from .Canvas import Canvas

DISPLAY_CLASS_NAME_POSTFIX = "Display"

class BoundariesTouching():
    def __init__(self, left: bool, right: bool, top: bool, bottom: bool):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
    
    def is_touching_left_boundary(self) -> bool:
        return self.left
    
    def is_touching_right_boundary(self) -> bool:
        return self.right
    
    def is_touching_top_boundary(self) -> bool:
        return self.top
    
    def is_touching_bottom_boundary(self) -> bool:
        return self.bottom

def compute_boundaries_touching(rectangle: Rectangle, bounding_rectangle: Rectangle) -> BoundariesTouching:
    left = rectangle.left == bounding_rectangle.left
    right = rectangle.right == bounding_rectangle.right
    top = rectangle.top == bounding_rectangle.top
    bottom = rectangle.bottom == bounding_rectangle.bottom
    return BoundariesTouching(left, right, top, bottom)

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

    def is_boundary_acknowledging(self) -> bool:
        return False
    
    @staticmethod
    def supports_grid(grid: Grid) -> bool:
        return True

    @classmethod
    def get_name(cls):
        instance = cls()
        name: str = instance.__class__.__name__[:-len(DISPLAY_CLASS_NAME_POSTFIX)]
        return name

class EmptyDisplay(Display):
    pass

class BoundaryAcknowledgingDisplay(Display):
    def draw_on(self, canvas: Canvas):
        self.draw_on_canvas_given_boundaries_touching(canvas, BoundariesTouching(True, True, True, True))

    def draw_on_canvas_given_boundaries_touching(self, canvas: Canvas, boundaries_touching: BoundariesTouching):
        pass

    def is_boundary_acknowledging(self) -> bool:
        return True

class FrameDisplay(BoundaryAcknowledgingDisplay): 
    '''Displays a grid around a rectangle showing the coordinates of the grid'''
    pass

class PositionDisplay(Display):
    '''Displays a grid within a rectangle showing the positions on the grid'''
    pass