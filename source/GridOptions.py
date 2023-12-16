from .Grid import Grid
from typing import List
from talon import Module, actions

class GridOption:
    def __init__(self, name: str, factory_name: str, default_display_option: str, argument: str = ""):
        self.name = name
        self.factory_name = factory_name
        self.default_display_option = default_display_option
        self.argument = argument
    
    def get_name(self) -> str:
        return self.name

    def get_factory_name(self) -> str:
        return self.factory_name

    def get_default_display_option(self) -> str:
        return self.default_display_option

    def get_argument(self) -> str:
        return self.argument

class GridOptions:
    def __init__(self, options: List[GridOption]):
        self.options = {option.get_name():option for option in options}
    
    def get_option(self, name: str) -> GridOption:
        return self.options[name]

options = []
grid_options = GridOptions(options)

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_create_grid_from_option(name: str) -> Grid:
        '''Creates the specified mouse control chicken grid from the available grid options'''
        option = GridOptions.get_option(name)
        grid = actions.user.mouse_control_chicken_create_grid_from_factory(option.get_factory_name(), option.get_argument())
        return grid
