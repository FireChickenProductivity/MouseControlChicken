from .Grid import Grid
from .Display import Display
from .RectangleManager import RectangleManager, ScreenRectangleManager, CurrentWindowRectangleManager
from .SettingsMediator import settings_mediator
from talon import Module, actions

class GridSystemManager:
    def __init__(self):
        self.grid: Grid = None
        self.display: Display = None
        self.rectangle_manager: RectangleManager = ScreenRectangleManager()
    
    def set_grid(self, grid: Grid):
        self.grid = grid
        self.refresh()

    def set_display(self, display: Display):
        self.display = display
        self.refresh()

    def set_rectangle_manager(self, rectangle_manager: RectangleManager):
        self.rectangle_manager = rectangle_manager
        self.refresh()
    
    def get_grid(self) -> Grid:
        return self.grid

    def refresh(self):
        if self.grid and self.display:
            self.grid.make_around(self.rectangle_manager.compute_rectangle())
            self.display.hide()
            self.display.set_grid(self.grid)
            self.display.show()

manager = GridSystemManager()

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_make_grid_around_screen():
        '''Makes the mouse control chicken grid form around a screen'''
        manager.set_rectangle_manager(ScreenRectangleManager())
    
    def mouse_control_chicken_make_grid_around_window():
        '''Makes the mouse control chicken grid form around the current window'''
        manager.set_rectangle_manager(CurrentWindowRectangleManager())