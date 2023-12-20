from talon import Module, actions, imgui
from typing import List

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
        for option in self.options: gui.text(option)

    
    def get_items_per_page(self):
        return self.items_per_page



information: OptionsDisplayInformation = None
@imgui.open(y = 0)
def gui(gui: imgui.GUI):
    if information: information.display_on(gui)

