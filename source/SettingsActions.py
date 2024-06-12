from talon import Module
from .SettingsMediator import settings_mediator

module = Module()

def is_valid_transparency(transparency: int) -> bool:
    return transparency >= 0 and transparency <= 100

def convert_transparency_to_float(transparency: int) -> float:
    return transparency / 100.0

@module.action_class
class Actions:
    def mouse_control_chicken_toggle_frame_display_crisscross():
        '''Toggles whether mouse control chicken frame displays should show  crisscrossing lines'''
        settings_mediator.set_frame_grid_should_show_crisscross(not settings_mediator.get_frame_grid_should_show_crisscross())

    def mouse_control_chicken_set_checker_frequency(frequency: int):
        '''Sets the mouse control chicken checker frequency'''
        settings_mediator.set_checker_frequency(frequency)

    def mouse_control_chicken_set_zigzag_threshold(threshold: int):
        '''Sets the mouse control chicken zigzag threshold'''
        settings_mediator.set_zigzag_threshold(threshold)

    def mouse_control_chicken_refresh():
        '''Refreshes the mouse control chicken grid and reloads settings from their defaults'''
        settings_mediator.restore_default_settings()
    
    def mouse_control_chicken_set_text_size(size: int):
        '''Sets the mouse control chicken text size'''
        if size > 0:
            settings_mediator.set_text_size(size)

    def mouse_control_chickens_set_main_transparency(transparency: int):
        '''Sets the mouse control chicken main transparency'''
        if is_valid_transparency(transparency):
            converted_transparency = convert_transparency_to_float(transparency)
            settings_mediator.set_main_transparency(converted_transparency)
        
    def mouse_control_chickens_set_background_transparency(transparency: int):
        '''Sets the mouse control chicken background transparency'''
        if is_valid_transparency(transparency):
            converted_transparency = convert_transparency_to_float(transparency)
            settings_mediator.set_background_transparency(converted_transparency)
        
    def mouse_control_chickens_set_line_width(width: int):
        '''Sets the mouse control chicken line width'''
        if width > 0:
            settings_mediator.set_line_width(width)
        
@module.capture(rule = '<number_small>|one hundred')
def mouse_control_chicken_percentage(m) -> int:
    number_text = m[0]
    if number_text == 'one':
        return 100
    return int(number_text)