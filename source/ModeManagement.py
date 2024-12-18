from talon import Module, actions, Context

module = Module()
narrow_able_grid_mode_name = "mouse_control_chicken_narrow_able_grid_mode"
narrow_able_grid_mode = 'user.' + narrow_able_grid_mode_name
module.mode(narrow_able_grid_mode_name, desc = "A mode for working with a narrow able mouse control chicken grid")

scroll_mode_name = "mouse_control_chicken_scroll_mode"
scroll_mode = 'user.' + scroll_mode_name
module.mode(scroll_mode_name, desc = "The mode activated during mouse control chicken repeated scrolling")

def enable_mode(mode: str):
    actions.mode.save()
    actions.mode.disable("command")
    actions.mode.disable("dictation")
    actions.mode.enable(mode)

def disable_mode(mode: str):
    actions.mode.disable(mode)
    actions.mode.restore()

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_enable_narrow_able_grid_mode():
        '''Enables the narrow able mouse control chicken grid mode'''
        enable_mode(narrow_able_grid_mode)
    
    def mouse_control_chicken_enable_scroll_mode():
        '''Enables the mouse control chicken scroll mode'''
        enable_mode(scroll_mode)
    
    def mouse_control_chicken_disable_scroll_mode():
        '''Disables the mouse control chicken scroll mode'''
        disable_mode(scroll_mode)
    
    def mouse_control_chicken_disable_narrow_able_grid_mode():
        '''Disables the narrow able mouse control chicken grid mode'''
        actions.mode.disable(narrow_able_grid_mode)

narrow_able_grid_mode_context = Context()
narrow_able_grid_mode_context.matches = r"""
mode: user.mouse_control_chicken_narrow_able_grid_mode
"""
@narrow_able_grid_mode_context.action_class("user")
class NarrowAbleGridModeActions:
    def mouse_control_chicken_disable_narrow_able_grid_mode():
        '''Disables the narrow able mouse control chicken grid mode'''
        actions.mode.disable(narrow_able_grid_mode)
        actions.mode.restore()