from .OptionsDialogue import OptionsDialogueInformation
from ..TagManagement import DICTATION_INPUT_WITH_OPTIONS_TAG, PAGE_ADJUSTMENT_TAG
from ..ContextUtilities import create_context_matches_single_tag_string
from talon import Module, actions, imgui, Context
from typing import Callable, List

title = None
dictation_input = None
acceptance_callback: Callable[[str], None] = None
cancellation_callback: Callable[[], None] = None
options_information: OptionsDialogueInformation = None

DICTATION_INPUT_CAPTURE = "user.mouse_control_chicken_dictation_input"

@imgui.open(y = 0)
def gui(gui: imgui.GUI):
    if title: gui.text(title)
    show_commands_on(gui)
    if dictation_input: gui.text(dictation_input)
    if options_information: show_options_information_on(gui)

def show_commands_on(gui: imgui.GUI):
    gui.line()
    gui.text("choose <text>: chooses the dictated text")
    gui.text("accept: accepts the current text input")
    gui.text("cancel or reject: cancels the current text input")
    gui.line()

def show_options_information_on(gui: imgui.GUI):
    gui.line()
    options_information.show_on(gui)

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_show_dictation_input_dialogue_with_title_acceptance_callback_and_cancellation_callback(
            new_title: str,
            new_acceptance_callback: Callable[[str], None], 
            new_cancellation_callback: Callable[[], None]
        ):
        '''Shows dictation input for mouse control chicken'''
        actions.user.mouse_control_chicken_show_dictation_input_dialogue_with_title_acceptance_callback_cancellation_callback_and_tag_names(
            new_title, 
            new_acceptance_callback, 
            new_cancellation_callback, 
            []
        )

    def mouse_control_chicken_show_dictation_input_dialogue_with_title_acceptance_callback_cancellation_callback_and_tag_names(
            new_title: str, 
            new_acceptance_callback: Callable[[str], None], 
            new_cancellation_callback: Callable[[], None], 
            tag_names: List[str]
        ):
        '''Shows dictation input for mouse control chicken with a tag name'''
        erase_dictation_input_data()
        actions.user.mouse_control_chicken_hide_dictation_input_dialogue()
        global title
        title = new_title
        global acceptance_callback
        acceptance_callback = new_acceptance_callback
        global cancellation_callback
        cancellation_callback = new_cancellation_callback
        actions.user.mouse_control_chicken_enable_dictation_input_dialogue_tag(tag_names)
        gui.show()

    def mouse_control_chicken_hide_dictation_input_dialogue():
        '''Hides the dictation input dialogue for mouse control chicken'''
        actions.user.mouse_control_chicken_disable_dictation_input_dialogue_tag()
        gui.hide()

    def mouse_control_chicken_accept_dictation_input():
        '''Accepts the current dictation input for mouse control chicken'''
        global acceptance_callback
        global dictation_input
        global options_information
        callback = acceptance_callback
        input = dictation_input
        if options_information: input = options_information.get_item_on_page_from_number(int(input))
        actions.user.mouse_control_chicken_hide_dictation_input_dialogue()
        erase_dictation_input_data()
        callback(input)

    def mouse_control_chicken_cancel_dictation_input():
        '''Cancels taking dictation input for mouse control chicken'''
        global cancellation_callback
        cancellation_callback()
        actions.user.mouse_control_chicken_hide_dictation_input_dialogue()
        erase_dictation_input_data()

    def mouse_control_chicken_set_dictation_input_dialogue_text(text: str):
        '''Sets the text of the mouse control chicken dictation input dialogue'''
        global dictation_input
        dictation_input = text
    
    def mouse_control_chicken_show_dictation_input_dialogue_with_title_acceptance_callback_cancellation_callback_tag_names_and_options(
            new_title: str, 
            new_acceptance_callback: Callable[[str], None], 
            new_cancellation_callback: Callable[[], None], 
            tag_names: List[str], 
            options: List[str]
        ):
        '''Shows the dictation input dialogue for mouse control chicken with the specified options'''
        actions.user.mouse_control_chicken_show_dictation_input_dialogue_with_title_acceptance_callback_cancellation_callback_and_tag_names(
            new_title, 
            new_acceptance_callback, 
            new_cancellation_callback, 
            tag_names + [PAGE_ADJUSTMENT_TAG, DICTATION_INPUT_WITH_OPTIONS_TAG]
        )
        global options_information
        options_information = OptionsDialogueInformation("Options:", options)

def erase_dictation_input_data():
    global dictation_input
    dictation_input = None
    global title
    title = None
    global acceptance_callback
    acceptance_callback = None
    global cancellation_callback
    cancellation_callback = None
    erase_options_information()

def erase_options_information():
    global options_information
    options_information = None

@module.capture(rule = "<user.text>")
def mouse_control_chicken_dictation_input(m) -> str:
    '''Dictation input given to a mouse control chicken dialogue'''
    return m.text

context = Context()
context.matches = create_context_matches_single_tag_string(DICTATION_INPUT_WITH_OPTIONS_TAG)
@context.action_class("user")
class UserActions:
    def mouse_control_chicken_advance_options_dialogue_page():
        '''Advances the page for the mouse control chicken options dialogue'''
        global options_information
        options_information.advance_page()
    
    def mouse_control_chicken_return_to_previous_options_dialogue_page():
        '''Returns the page to the previous page for the mouse control chicken options dialogue'''
        global options_information
        options_information.go_to_previous_page()