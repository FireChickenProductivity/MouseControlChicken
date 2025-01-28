from talon import actions, Module

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_close_all_dialogues():
        '''Closes all open dialogues'''
        actions.user.mouse_control_chicken_hide_options_dialogue()
        actions.user.mouse_control_chicken_exit_dictation_input()
