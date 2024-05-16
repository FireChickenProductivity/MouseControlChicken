from .grid.Grid import Rectangle
from .SettingsMediator import settings_mediator
from talon import ui, Module, ui, cron

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

class WindowTrackingRectangleManager(RectangleManager):
    def __init__(self, sensitive_focus_switching: bool = False):
        super().__init__()
        self.current_window_rectangle_manager = CurrentWindowRectangleManager()
        self.registration_targets = ['win_focus']
        if sensitive_focus_switching:
            self.registration_targets += ['win_move, win_resize']
        for target in self.registration_targets:
            ui.register(target, lambda window: self.update_rectangle(target, window))
        self.last_window_rectangle = None
        self.update_job = None
    
    def update_rectangle(self, cause, window):
        new_rectangle = convert_talon_rectangle_to_rectangle(window.rect)
        if window and (not self.last_window_rectangle or new_rectangle != self.last_window_rectangle) and (window.title != 'Talon Canvas'):
            print('updating window', cause, window, self.last_window_rectangle, new_rectangle)
            if self.update_job:
                cron.cancel(self.update_job)
            self.update_job = cron.after('1s', self.call_callback)
        elif window and self.last_window_rectangle and new_rectangle == self.last_window_rectangle:
            cron.cancel(self.update_job)
            self.update_job = None
            print('canceling')

    def compute_rectangle(self) -> Rectangle:
        self.last_window_rectangle = self.current_window_rectangle_manager.compute_rectangle()
        return self.current_window_rectangle_manager.compute_rectangle()

    def deactivate(self):
        for target in self.registration_targets:
            ui.unregister(target, self.update_rectangle)
        
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

def add_amount_to_screen_number(amount: int):
    screen_number = settings_mediator.get_current_screen_number() + amount
    screen_number = compute_corrected_screen_number(screen_number)
    settings_mediator.set_current_screen_number(screen_number)

def compute_corrected_screen_number(screen_number: int) -> int:
    screens = ui.screens()
    if screen_number >= len(screens): screen_number = 0
    if screen_number < 0: screen_number = len(screens) - 1
    return screen_number