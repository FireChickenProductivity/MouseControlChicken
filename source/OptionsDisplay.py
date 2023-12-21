from talon import Module, actions, imgui
from typing import List, Callable


class OptionsDisplayInformation:
    def __init__(self, title: str, options: List[str]):
        self.title = title
        self.options = options
        self.page_number = 1
        self.items_per_page = 10
        self.compute_page()

    def compute_page(self):
        starting_index = (self.page_number - 1)*self.items_per_page
        ending_index = self.page_number*self.items_per_page
        self.page = self.options[starting_index:ending_index]
    
    def advance_page(self):
        self.page_number += 1
        self.page_number = self.page_number % (len(self.options)//self.items_per_page)
        self.compute_page()
    
    def go_to_previous_page(self):
        if self.page_number > 1: self.page_number -= 1
        self.compute_page()
    
    def display_on(self, gui: imgui.GUI):
        gui.text(self.title)
        gui.line()
        for index, option in enumerate(self.page): gui.text(f'{index + 1}: {option}')
    
    def get_item_on_page_from_number(self, number: int) -> str:
        return self.page[number - 1]

    def get_items_per_page(self):
        return self.items_per_page



information: OptionsDisplayInformation = None
callback = None
@imgui.open(y = 0)
def gui(gui: imgui.GUI):
    if information: information.display_on(gui)

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_show_options_display_with_options_title_tag_and_callback(options: List[str], title: str, tag: str, new_callback: Callable[[str], None]):
        '''Shows options for mouse control chicken'''
        actions.user.mouse_control_chicken_hide_options_display()
        global information
        information = OptionsDisplayInformation(title, options)
        global callback
        callback = new_callback
        gui.show()
    
    def mouse_control_chicken_hide_options_display():
        '''Hides the options display for mouse control chicken'''
        if gui.showing: gui.hide()
        global callback
        callback = None
    
    def mouse_control_chicken_choose_option_from_display(number: int):
        '''Chooses the option from the mouse controlled chicken options display'''
        if callback and information:
            option_text: str = information.get_item_on_page_from_number(number)
            callback(option_text)
    
    def mouse_control_chicken_advance_options_display_page():
        '''Advances the display page for the mouse control chicken display options'''
        information.advance_page()

    def mouse_control_chicken_return_to_previous_options_display_page():
        '''Returns the display page to the previous page for the mouse control chicken display options'''
        information.go_to_previous_page()