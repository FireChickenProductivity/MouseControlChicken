from .Grid import Grid, Rectangle
from .Canvas import Canvas
DISPLAY_CLASS_NAME_POSTFIX = "Display"

class Display:
    def set_grid(self, grid: Grid): pass
    def set_rectangle(self, rectangle: Rectangle): pass
    def show(self):
        if self.canvas:
            self.canvas.show()
    def hide(self):
        if self.canvas:
            self.canvas.hide()
    def refresh(self):
        if self.canvas:
            self.canvas.refresh()
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

class CrisscrossDisplay(Display):
    '''Displays a grid within a rectangle by showing positions on the grid with criss crossing horizontal and vertical lines'''
    pass

class PositionDisplay(Display):
    '''Displays a grid within a rectangle showing the positions on the grid'''
    pass


