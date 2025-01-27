from .grid.Grid import Rectangle
from .SettingsMediator import settings_mediator
from talon import ui, Module,  actions, app, cron

class RectangleManager:
    def __init__(self):
        self.callback = None
        
    def set_callback(self, callback):
        self.callback = callback
    
    def call_callback(self):
        if self.callback: self.callback()

    def deactivate(self): pass

    def compute_rectangle(self) -> Rectangle: pass

class ScreenRectangleManager(RectangleManager):
    def compute_rectangle(self) -> Rectangle:
        screens = ui.screens()
        screen = screens[settings_mediator.get_current_screen_number()]
        talon_rectangle = screen.rect
        rectangle = convert_talon_rectangle_to_rectangle(talon_rectangle)
        return rectangle

class CurrentWindowRectangleManager(RectangleManager):
    def compute_rectangle(self) -> Rectangle:
        window = ui.active_window()
        try:
            talon_rectangle = window.rect
            rectangle = convert_talon_rectangle_to_rectangle(talon_rectangle)
        except:
            rectangle = ScreenRectangleManager().compute_rectangle()
        return rectangle

def call_after_window_following_delay(callback):
    cron.after(f"{settings_mediator.get_window_following_delay()}ms", callback)

class WindowTrackingRectangleManager(RectangleManager):
    def __init__(self, sensitive_focus_switching: bool = True):
        super().__init__()
        self.current_window_rectangle_manager = CurrentWindowRectangleManager()
        self.registration_targets = ['win_focus']
        if sensitive_focus_switching:
            self.registration_targets.extend(['win_move', 'win_resize'])
        for target in self.registration_targets:
            ui.register(target, lambda window: self.update_rectangle(target, window))
        self.last_window_rectangle = None
        self.active = True
    
    def _update_rectangle_helper(self, window):
        new_rectangle = self.current_window_rectangle_manager.compute_rectangle()
        if self.active and window == ui.active_window() and (not self.last_window_rectangle or new_rectangle != self.last_window_rectangle):
            self.call_callback()

    def update_rectangle(self, cause, window):
        call_after_window_following_delay(lambda: self._update_rectangle_helper(window))

    def compute_rectangle(self) -> Rectangle:
        self.last_window_rectangle = self.current_window_rectangle_manager.compute_rectangle()
        return self.last_window_rectangle

    def deactivate(self):
        self.active = False
        for target in self.registration_targets:
            ui.unregister(target, self.update_rectangle)

class ScreenTrackingRectangleManager(RectangleManager):
    def __init__(self):
        super().__init__()
        self.window_tracker = WindowTrackingRectangleManager(sensitive_focus_switching=True)
        self.window_tracker.set_callback(self.update_rectangle)
        self.last_rectangle = ScreenRectangleManager().compute_rectangle()
        self.update_rectangle()
    
    def update_rectangle(self):
        window = ui.active_window()
        window_rectangle = None
        try:
            window_rectangle = window.rect
            screen_rectangle = ui.screen_containing(*window_rectangle.center).rect
            new_rectangle = convert_talon_rectangle_to_rectangle(screen_rectangle)
        except:
            new_rectangle = ScreenRectangleManager().compute_rectangle()
        if not self.last_rectangle or new_rectangle != self.last_rectangle:
            self.last_rectangle = new_rectangle
            self.call_callback()
    
    def compute_rectangle(self) -> Rectangle:
        '''Returns the rectangle of the screen that the active window is on'''
        return self.last_rectangle
    
    def deactivate(self):
        self.window_tracker.deactivate()

def convert_talon_rectangle_to_rectangle(talon_rectangle):
    return Rectangle(talon_rectangle.y, talon_rectangle.y + talon_rectangle.height, talon_rectangle.x, talon_rectangle.x + talon_rectangle.width)

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_use_next_screen():
        '''Updates the mouse control chicken grid screen to the next one'''
        add_amount_to_screen_number(1)

    def mouse_control_chicken_use_previous_screen():
        '''Updates the mouse control chicken grid screen to the previous one'''
        add_amount_to_screen_number(-1)
    
    def mouse_control_chicken_use_screen(screen_number: int):
        '''Updates the mouse control chicken grid screen to the specified one'''
        new_screen_number = compute_corrected_screen_number(screen_number - 1)
        settings_mediator.set_current_screen_number(new_screen_number)
    
    def mouse_control_chicken_set_rectangle_manager_to_window():
        '''Has mouse control chicken manage the active rectangle using the window rectangle manager'''
        rectangle_manager = CurrentWindowRectangleManager()
        actions.user.mouse_controlled_chicken_set_rectangle_manager(rectangle_manager)

    def mouse_control_chicken_set_rectangle_manager_to_screen():
        '''Has mouse control chicken manage the active rectangle using the screen rectangle manager'''
        rectangle_manager = ScreenRectangleManager()
        actions.user.mouse_controlled_chicken_set_rectangle_manager(rectangle_manager)
    
    def mouse_control_chicken_set_rectangle_manager_to_follow_window():
        '''Has mouse control chicken have the active rectangle follow the active window'''
        actions.user.mouse_controlled_chicken_set_rectangle_manager(WindowTrackingRectangleManager())
    
    def mouse_control_chicken_set_rectangle_manager_to_follow_screen():
        '''Has mouse control chicken have the active rectangle follow the active screen'''
        actions.user.mouse_controlled_chicken_set_rectangle_manager(ScreenTrackingRectangleManager())

def add_amount_to_screen_number(amount: int):
    screen_number = settings_mediator.get_current_screen_number() + amount
    screen_number = compute_corrected_screen_number(screen_number)
    settings_mediator.set_current_screen_number(screen_number)

def compute_corrected_screen_number(screen_number: int) -> int:
    screens = ui.screens()
    if screen_number >= len(screens): screen_number = 0
    if screen_number < 0: screen_number = len(screens) - 1
    return screen_number

def create_default_rectangle_manager():
    default_rectangle_manager_setting = settings_mediator.get_default_rectangle_manager()
    result = ScreenRectangleManager()
    if default_rectangle_manager_setting == 'window':
        result = CurrentWindowRectangleManager()
    elif default_rectangle_manager_setting == 'screen':
        result = ScreenRectangleManager()
    elif default_rectangle_manager_setting == 'follow window':
        result = WindowTrackingRectangleManager()
    elif default_rectangle_manager_setting == 'follow screen':
        result = ScreenTrackingRectangleManager()
    else:
        app.notify(f'Unknown default rectangle manager setting: {default_rectangle_manager_setting}')
    return result