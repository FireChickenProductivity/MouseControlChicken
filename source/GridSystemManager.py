from .Grid import Grid
from .Display import Display
from .RectangleManager import RectangleManager, ScreenRectangleManager, CurrentWindowRectangleManager

class GridSystemManager:
    def __init__(self):
        self.grid: Grid = None
        self.display: Display = None
        self.rectangle_manager: RectangleManager = ScreenRectangleManager
    
    def set_grid(self, grid: Grid):
        self.grid = grid
        self.refresh()

    def set_display(self, display: Display):
        self.display = display
        self.refresh()

    def set_rectangle_manager(self, rectangle_manager: RectangleManager):
        self.rectangle_manager = rectangle_manager
        self.refresh()
    
    def refresh(self):
        if self.grid and self.display:
            self.grid.make_around(self.rectangle_manager.compute_rectangle())
            self.display.hide()
            self.display.set_grid(self.grid)
            self.display.show()