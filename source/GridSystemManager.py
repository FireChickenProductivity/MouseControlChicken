from .Grid import Grid, Rectangle, RecursivelyDivisibleGrid
from .display.Display import Display
from .Callbacks import NoArgumentCallback
from .SettingsMediator import settings_mediator
from .RectangleManagement import RectangleManager, ScreenRectangleManager, CurrentWindowRectangleManager
from .GridOptions import GridOptions
from .display.DisplayOptionsComputer import compute_display_options_given_grid, compute_display_options_names_given_grid
from .fire_chicken.mouse_position import MousePosition
from .GridOptionsList import update_option_default_display
from .DisplayManagement import DisplayManager
from talon import Module, actions, app

class GridSystemManager:
    def __init__(self):
        self.grid: Grid = None
        self.display_manager: DisplayManager = DisplayManager()
        self.rectangle_manager: RectangleManager = ScreenRectangleManager()
        self.should_load_default_grid_next: bool = True
    
    def set_grid(self, grid: Grid):
        self.grid = grid
        if self.has_received_first_grid():
            self.should_load_default_grid_next = False
        self.refresh()
        
    def has_received_first_grid(self) -> bool:
        return self.should_load_default_grid_next and self.grid

    def set_display(self, display: Display):
        self.display_manager.set_display(display)
        self.refresh()

    def set_rectangle_manager(self, rectangle_manager: RectangleManager):
        self.rectangle_manager = rectangle_manager
        self.refresh()
    
    def get_grid(self) -> Grid:
        return self.grid

    def get_display(self) -> Display:
        return self.display_manager.get_display()

    def refresh(self):
        self.hide()
        if self.grid and self.display_manager.has_display():
            rectangle = self.rectangle_manager.compute_rectangle()
            self.grid.make_around(rectangle)
            self.display_manager.refresh_display(self.grid, rectangle)
            actions.user.mouse_control_chicken_enable_grid_showing_tags(self.grid)

    def prepare_for_grid_switch(self):
        self.set_display(None)
        self.set_grid(None)
    
    def hide(self):
        self.display_manager.hide()
        actions.user.mouse_control_chicken_disable_grid_showing_tags()
    
    def show(self):
        if not self.grid and self.should_load_default_grid_next:
            actions.user.mouse_control_chicken_choose_grid_from_options(settings_mediator.get_default_grid_option())
        self.refresh()
        
manager: GridSystemManager = None
current_option: str = None

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
        '''Updates the mouse control chicken current grid to the specified grid option'''
        global current_option
        current_option = name
        options: GridOptions = actions.user.mouse_control_chicken_get_grid_options()
        option = options.get_option(name)
        grid = actions.user.mouse_control_chicken_create_grid_from_factory(option.get_factory_name(), option.get_argument())
        display_options = compute_display_options_given_grid(grid)
        display = display_options.create_display_from_option(option.get_default_display_option())
        global manager
        manager.prepare_for_grid_switch()
        manager.set_display(display)
        manager.set_grid(grid)
    
    def mouse_control_chicken_choose_display_from_options(name: str):
        '''Changes the active mouse control chicken grid display based on the name of the option'''
        global manager
        display_options = compute_display_options_given_grid(manager.get_grid())
        display = display_options.create_display_from_option(name)
        manager.set_display(display)

    def mouse_control_chicken_show_grid_options():
        '''Shows the mouse control chicken grid options'''
        options: GridOptions = actions.user.mouse_control_chicken_get_grid_options()
        names = [name for name in options.get_option_names()]
        actions.user.mouse_control_chicken_show_options_dialogue_with_options_title_callback_and_tag(names, "Grid Options", actions.user.mouse_control_chicken_choose_grid_from_options)

    def mouse_control_chicken_show_display_options():
        '''Shows the mouse control chicken display options for the active grid'''
        show_display_options("Display Options", actions.user.mouse_control_chicken_choose_display_from_options)

    def mouse_control_chicken_show_default_display_options():
        '''Shows options for the new default grid for the active mouse control chicken grid'''
        show_display_options("Default Display Options", lambda display_name: update_option_default_display(current_option, display_name))

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
        position: MousePosition = actions.user.mouse_control_chicken_get_position_on_grid(coordinates)
        position.go()
    
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
            manager.refresh_display(grid, new_rectangle)

    def mouse_control_chicken_reset_narrow_able_grid():
        '''Resets the current mouse control chicken grid'''
        if manager_has_narrow_able_grid():
            manager.refresh()
            actions.user.mouse_control_chicken_disable_narrow_able_grid_mode()
    
    def mouse_control_chicken_get_current_position_on_narrow_able_grid() -> MousePosition:
        '''Gets the current position on the current mouse control chicken narrow able grid'''
        grid = manager.get_grid()
        position = grid.compute_current_position()
        return position
    
    def mouse_control_chicken_get_position_on_grid(coordinates: str) -> MousePosition:
        '''Gets the position on the current mouse control chicken grid'''
        grid = manager.get_grid()
        position = grid.compute_absolute_position_from(coordinates)
        return position
    
    def mouse_control_chicken_is_using_narrow_able_grid() -> bool:
        '''Returns whether the current mouse control chicken grid is narrow able'''
        return manager_has_narrow_able_grid()

def show_display_options(title: str, callback):
    grid = manager.get_grid()
    options_text = compute_display_options_names_given_grid(grid)
    actions.user.mouse_control_chicken_show_options_dialogue_with_options_title_callback_and_tag(options_text, title, callback)

def manager_has_narrow_able_grid() -> bool:
    grid = manager.get_grid()
    return grid and grid.supports_narrowing()

def drag_from_position():
    actions.sleep(0.5)
    actions.user.mouse_drag(0)

def end_drag_at_position():
    actions.sleep(0.5)
    actions.user.mouse_drag_end()

def double_click():
    actions.mouse_click()
    actions.mouse_click()

def scroll_up():
    actions.mouse_scroll(-settings_mediator.get_scrolling_amount())

def scroll_down():
    actions.mouse_scroll(settings_mediator.get_scrolling_amount())

def setup():
    global manager
    manager = GridSystemManager()
    register_on_change_callback()

def register_on_change_callback():
    callback = NoArgumentCallback(manager.refresh, manager.hide)
    callback_name = "manager_refresh"
    settings_mediator.register_on_change_callback(callback_name, callback)

app.register("ready", setup)