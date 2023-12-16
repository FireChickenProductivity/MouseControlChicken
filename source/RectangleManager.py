from .Grid import Rectangle
from .SettingsMediator import settings_mediator
from talon import ui

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