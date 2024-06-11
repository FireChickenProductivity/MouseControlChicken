from talon import Module
from .SettingsMediator import settings_mediator

module = Module()


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