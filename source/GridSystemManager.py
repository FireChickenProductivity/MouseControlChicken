from .Grid import Grid, Rectangle, RecursivelyDivisibleGrid
from .Display import Display
from .SettingsMediator import settings_mediator
from .RectangleManagement import RectangleManager, ScreenRectangleManager, CurrentWindowRectangleManager
from .GridOptions import GridOptions
from .DisplayOptionsComputer import DisplayOptionComputer
from .fire_chicken.mouse_position import MousePosition
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

    def get_display(self) -> Display:
        return self.display

    def refresh(self):
        if self.grid and self.display:
            rectangle = self.rectangle_manager.compute_rectangle()
            self.grid.make_around(rectangle)
            self.display.hide()
            self.display.set_grid(self.grid)
            self.display.set_rectangle(rectangle)
            self.display.show()
            actions.user.mouse_control_chicken_enable_grid_showing_tags(self.grid)

    def prepare_for_grid_switch(self):
        self.set_display(None)
        self.set_grid(None)
    
    def hide(self):
        if self.display: self.display.hide()
        actions.user.mouse_control_chicken_disable_grid_showing_tags()
    
    def show(self):
        self.refresh()
        
manager = GridSystemManager()
settings_mediator.register_on_change_callback(manager.refresh)

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
        manager.prepare_for_grid_switch()
        manager.set_display(display)
        manager.set_grid(grid)
    
    def mouse_control_chicken_choose_display_from_options(name: str):
        '''Changes the active mouse control chicken grid display based on the name of the option'''
        global manager
        display_options = DisplayOptionComputer().compute_display_options(manager.get_grid())
        display = display_options.create_display_from_option(name)
        manager.set_display(display)

    def mouse_control_chicken_show_grid_options():
        '''Shows the mouse control chicken grid options'''
        options: GridOptions = actions.user.mouse_control_chicken_get_grid_options()
        names = [name for name in options.get_option_names()]
        actions.user.mouse_control_chicken_show_options_display_with_options_title_callback_and_tag(names, "Grid Options", actions.user.mouse_control_chicken_choose_grid_from_options)

    def mouse_control_chicken_show_display_options():
        '''Shows the mouse control chicken display options for the active grid'''
        grid = manager.get_grid()
        display_options = DisplayOptionComputer().compute_display_options(grid)
        options_text = [option for option in display_options.get_names()]
        actions.user.mouse_control_chicken_show_options_display_with_options_title_callback_and_tag(options_text, "Display Options", actions.user.mouse_control_chicken_choose_display_from_options)

    def mouse_control_chicken_hide_grid():
        '''Hides the mouse control chicken grid'''
        global manager
        manager.hide()
    
    def mouse_control_chicken_show_grid():
        '''Shows the mouse control chicken grid'''
        global manager
        manager.show()
    
    def mouse_control_chicken_move_to_position(coordinates: str):
        '''Moves the mouse to the specified position on the current mouse control chicken grid'''
        position: MousePosition = get_position_on_grid(coordinates)
        position.go()

    def mouse_control_chicken_click_position(coordinates: str):
        '''Clicks the specified position on the current mouse control chicken grid'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        actions.mouse_click()
    
    def mouse_control_chicken_right_click_position(coordinates: str):
        '''Clicks the specified position on the current mouse control chicken grid'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        actions.mouse_click(1)
    
    def mouse_control_chicken_drag_from_position(coordinates: str):
        '''Moves the mouse to the specified position on the current mouse control chicken position and starts dragging'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        drag_from_position()
    
    def mouse_control_chicken_end_drag_at_position(coordinates: str):
        '''Moves the mouse to the specified position on the current mouse control chicken position and stops dragging'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        actions.sleep(0.5)
        actions.user.mouse_drag_end()

    def mouse_control_chicken_set_rectangle_manager_to_window():
        '''Has mouse control chicken manage the active rectangle using the window rectangle manager'''
        rectangle_manager = CurrentWindowRectangleManager()
        manager.set_rectangle_manager(rectangle_manager)

    def mouse_control_chicken_set_rectangle_manager_to_screen():
        '''Has mouse control chicken manage the active rectangle using the screen rectangle manager'''
        rectangle_manager = ScreenRectangleManager()
        manager.set_rectangle_manager(rectangle_manager)

    def mouse_control_chicken_narrow_grid(coordinates: str):
        '''Narrows the current mouse control chicken grid using the specified coordinates'''
        if manager_has_narrow_able_grid():
            grid: RecursivelyDivisibleGrid = manager.get_grid()
            new_rectangle: Rectangle = grid.compute_sub_rectangle_for(coordinates)
            grid.narrow_grid_using_coordinates(coordinates)
            display = manager.get_display()
            display.hide()
            display.set_grid(grid)
            display.set_rectangle(new_rectangle)
            display.show()

    def mouse_control_chicken_reset_narrow_able_grid():
        '''Resets the current mouse control chicken grid'''
        if manager_has_narrow_able_grid():
            manager.refresh()
    
    def mouse_control_chicken_click_current_position_on_narrow_able_grid():
        '''Clicks the current position on the current mouse control chicken grid'''
        if manager_has_narrow_able_grid():
            position = get_current_position_on_narrow_able_grid()
            position.go()
            actions.mouse_click()
            actions.user.mouse_control_chicken_reset_narrow_able_grid()
        
    def mouse_control_chicken_right_click_current_position_on_narrow_able_grid():
        '''Right clicks the current position on the current mouse control chicken grid'''
        if manager_has_narrow_able_grid():
            position = get_current_position_on_narrow_able_grid()
            position.go()
            actions.mouse_click(1)
            actions.user.mouse_control_chicken_reset_narrow_able_grid()
        
    def mouse_control_chicken_drag_from_current_position_on_narrow_able_grid():
        '''Starts dragging from the current position on the current mouse control chicken grid'''
        if manager_has_narrow_able_grid():
            position = get_current_position_on_narrow_able_grid()
            position.go()
            drag_from_position()
            actions.user.mouse_control_chicken_reset_narrow_able_grid()

def get_position_on_grid(coordinates: str) -> MousePosition:
    grid = manager.get_grid()
    position = grid.compute_absolute_position_from(coordinates)
    return position

def get_current_position_on_narrow_able_grid() -> MousePosition:
    grid = manager.get_grid()
    position = grid.compute_current_position()
    return position

def manager_has_narrow_able_grid() -> bool:
    grid = manager.get_grid()
    return grid and grid.supports_narrowing()

def drag_from_position():
    actions.sleep(0.5)
    actions.user.mouse_drag(0)