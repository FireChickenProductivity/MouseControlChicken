from .Grid import Grid
from .Display import Display
from .RectangleManager import RectangleManager, ScreenRectangleManager, CurrentWindowRectangleManager
from .SettingsMediator import settings_mediator
from .GridOptions import GridOptions
from .DisplayOptionsComputer import DisplayOptionComputer
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
        if self.display: self.display.hide()
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

    def hide(self):
        if self.display: self.display.hide()
    
    def show(self):
        self.refresh()
        
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
    
    def mouse_control_chicken_choose_grid_from_options(name: str):
        '''Updates the current grid to the specified grid option'''
        options: GridOptions = actions.user.mouse_control_chicken_get_grid_options()
        option = options.get_option(name)
        grid = actions.user.mouse_control_chicken_create_grid_from_factory(option.get_factory_name(), option.get_argument())
        display_options = DisplayOptionComputer().compute_display_options(grid)
        display = display_options.create_display_from_option(option.get_default_display_option())
        global manager
        manager.hide()
        manager.set_display(display)
        manager.set_grid(grid)
    
    def mouse_control_chicken_hide_grid():
        '''Hides the mouse control chicken grid'''
        global manager
        manager.hide()
    
    def mouse_control_chicken_show_grid():
        '''Shows the mouse control chicken grid'''
        global manager
        manager.show()