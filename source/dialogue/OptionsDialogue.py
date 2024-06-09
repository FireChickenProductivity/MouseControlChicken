from talon import Module, actions, imgui
from typing import List, Callable

class OptionsDialogueInformation:
    def __init__(self, title: str, options: List[str]):
        self.title = title
        self.options = options
        self.page_number = 1
        self.items_per_page = 15
        self.compute_page()

    def compute_page(self):
        starting_index = (self.page_number - 1)*self.items_per_page
        ending_index = self.page_number*self.items_per_page
        self.page = self.options[starting_index:ending_index]
    
    def advance_page(self):
        self.page_number += 1
        number_of_pages = self.compute_number_of_pages()
        if self.page_number > number_of_pages: self.page_number = number_of_pages
        self.compute_page()
    
    def compute_number_of_pages(self) -> int:
        return len(self.options)//self.items_per_page + 1
    
    def go_to_previous_page(self):
        if self.page_number > 1: self.page_number -= 1
        self.compute_page()
    
    def show_on(self, gui: imgui.GUI):
        gui.text(self.title)
        gui.line()
        for index, option in enumerate(self.page): gui.text(f'{index + 1}: {option}')
    
    def get_item_on_page_from_number(self, number: int) -> str:
        return self.page[number - 1]

    def get_items_per_page(self):
        return self.items_per_page



information: OptionsDialogueInformation = None
callback = None
@imgui.open(y = 0)
def gui(gui: imgui.GUI):
    if information: information.show_on(gui)

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_show_options_dialogue_with_options_title_callback_and_tag(options: List[str], title: str, new_callback: Callable[[str], None], tag: str = ""):
        '''Shows options for mouse control chicken'''
        actions.user.mouse_control_chicken_hide_options_dialogue()
        global information
        information = OptionsDialogueInformation(title, options)
        global callback
        callback = new_callback
        actions.user.mouse_control_chicken_enable_options_dialogue_tag(tag)
        gui.show()
    
    def mouse_control_chicken_hide_options_dialogue():
        '''Hides the options dialogue for mouse control chicken'''
        actions.user.mouse_control_chicken_disable_options_dialogue_tag()
        if gui.showing: gui.hide()
        global callback
        callback = None
    
    def mouse_control_chicken_choose_option_from_dialogue(number: int):
        '''Chooses the option from the mouse controlled chicken options dialogue'''
        if callback and information:
            option_text: str = information.get_item_on_page_from_number(number)
            callback(option_text)
    
    def mouse_control_chicken_advance_options_dialogue_page():
        '''Advances the page for the mouse control chicken options dialogue'''
        information.advance_page()

    def mouse_control_chicken_return_to_previous_options_dialogue_page():
        '''Returns the page to the previous page for the mouse control chicken options dialogue'''
        information.go_to_previous_page()