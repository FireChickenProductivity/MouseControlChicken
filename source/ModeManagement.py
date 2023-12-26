from talon import Module, actions, Context

module = Module()
narrow_able_grid_mode_name = "mouse_control_chicken_narrow_able_grid_mode"
narrow_able_grid_mode = 'user.' + narrow_able_grid_mode_name
module.mode(narrow_able_grid_mode_name, desc = "A mode for working with a narrow able mouse control chicken grid")

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_enable_narrow_able_grid_mode():
        '''Enables the narrow able mouse control chicken grid mode'''
        actions.mode.save()
        actions.mode.disable("command")
        actions.mode.disable("dictation")
        actions.mode.enable(narrow_able_grid_mode)
    
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
        print('restoring')