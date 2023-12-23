from .Grid import Rectangle
from .SettingsMediator import settings_mediator
from talon import ui, Module

class RectangleManager:
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
        talon_rectangle = window.rect
        rectangle = convert_talon_rectangle_to_rectangle(talon_rectangle)
        return rectangle


def convert_talon_rectangle_to_rectangle(talon_rectangle):
    return Rectangle(talon_rectangle.y, talon_rectangle.y + talon_rectangle.height, talon_rectangle.x, talon_rectangle.x + talon_rectangle.width)

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_use_next_screen():
        '''Updates the mouse control chicken grid screen to the next one'''
        screens = ui.screens()
        screen_number = settings_mediator.get_current_screen_number() + 1
        if screen_number >= len(screens): screen_number = 0
        settings_mediator.set_current_screen_number(screen_number)

    def mouse_control_chicken_use_previous_screen():
        '''Updates the mouse control chicken grid screen to the previous one'''
        screens = ui.screens()
        screen_number = settings_mediator.get_current_screen_number() - 1
        if screen_number >= len(screens): screen_number = 0
        if screen_number < 0: screen_number = len(screens) - 1
        settings_mediator.set_current_screen_number(screen_number)
