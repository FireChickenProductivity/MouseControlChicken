from .Grid import Grid
from typing import List
from talon import Module, actions

class GridOption:
    def __init__(self, name: str, factory_name: str, default_display_option: str, argument: str):
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
        self._set_options(options)
    
    def get_option(self, name: str) -> GridOption:
        return self.options[name]

    def get_option_names(self) -> List[str]:
        return self.options.keys()
    
    def _set_options(self, options: List[GridOption]):
        self.options = {option.get_name():option for option in options}
    
    def has_option(self, name: str) -> bool:
        return name in self.get_option_names()