from talon import Module, actions, imgui
from typing import Callable, List

title = None
dictation_input = None
acceptance_callback: Callable[[str], None] = None
cancellation_callback: Callable[[], None] = None

@imgui.open(y = 0)
def gui(gui: imgui.GUI):
    if title: gui.text(title)
    gui.line()
    gui.text("choose <text>: chooses the dictated text")
    gui.text("accept: accepts the current text input")
    gui.text("cancel or reject: cancels the current text input")
    gui.line()
    if dictation_input: gui.text(dictation_input)

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_show_dictation_input_display_with_title_acceptance_callback_and_cancellation_callback(
            new_title: str,
            new_acceptance_callback: Callable[[str], None], 
            new_cancellation_callback: Callable[[], None]
        ):
        '''Shows dictation input for mouse control chicken'''
        actions.user.mouse_control_chicken_show_dictation_input_display_with_title_acceptance_callback_cancellation_callback_and_tag_name(
            new_title, 
            new_acceptance_callback, 
            new_cancellation_callback, 
            []
        )

    def mouse_control_chicken_show_dictation_input_display_with_title_acceptance_callback_cancellation_callback_and_tag_names(
            new_title: str, 
            new_acceptance_callback: Callable[[str], None], 
            new_cancellation_callback: Callable[[], None], 
            tag_names: List[str]
        ):
        '''Shows dictation input for mouse control chicken with a tag name'''
        erase_dictation_input_data()
        actions.user.mouse_control_chicken_hide_dictation_input_display()
        global title
        title = new_title
        global acceptance_callback
        acceptance_callback = new_acceptance_callback
        global cancellation_callback
        cancellation_callback = new_cancellation_callback
        actions.user.mouse_control_chicken_enable_dictation_input_display_tag(tag_names)
        gui.show()

    def mouse_control_chicken_hide_dictation_input_display():
        '''Hides the dictation input display for mouse control chicken'''
        actions.user.mouse_control_chicken_disable_dictation_input_display_tag()
        gui.hide()

    def mouse_control_chicken_accept_dictation_input():
        '''Accepts the current dictation input for mouse control chicken'''
        global acceptance_callback
        acceptance_callback(dictation_input)
        actions.user.mouse_control_chicken_hide_dictation_input_display()
        erase_dictation_input_data()

    def mouse_control_chicken_cancel_dictation_input():
        '''Cancels taking dictation input for mouse control chicken'''
        global cancellation_callback
        cancellation_callback()
        actions.user.mouse_control_chicken_hide_dictation_input_display()
        erase_dictation_input_data()

    def mouse_control_chicken_set_dictation_input_display_text(text: str):
        '''Sets the text of the mouse control chicken dictation input display'''
        global dictation_input
        dictation_input = text
    
def erase_dictation_input_data():
    global dictation_input
    dictation_input = None
    global title
    title = None
    global acceptance_callback
    acceptance_callback = None
    global cancellation_callback
    cancellation_callback = None

@module.capture(rule = "<user.text>")
def mouse_control_chicken_dictation_input(m) -> str:
    '''Dictation input given to a mouse control chicken dialogue'''
    return m.text