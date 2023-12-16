from .Grid import Grid
from .RecursiveDivisionGrid import SquareRecursiveDivisionGrid
from .RectangularGrid import ListBasedGrid
from typing import List
from talon import Module

ONE_TO_NINE_GRID_NAME = "one to nine division"
ALPHABET_GRID_NAME = "Alphabet"

ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ]

class GridFactory:
    def create_grid(self, argument: str) -> Grid:
        pass

    def get_name() -> str:
        pass

    def matches_option(self, option: str) -> bool:
        return option == self.get_name()
    
    def get_arguments_description() -> str:
        return ""

class SquareRecursiveDivisionGridFactory:
    def create_grid(self, argument: str) -> Grid:
        argument = int(self.get_argument_text(argument))
        return SquareRecursiveDivisionGrid(argument)

    def get_name() -> str:
        return "Square Recursive Division Grid"
    
    def get_argument_text(self, option: str) -> str:
        return option[len(self.get_name()):]
    
    def get_arguments_description() -> str:
        return "A single integer. That integer squared gives the number of times to divide the rectangle."


class AlphabetGridFactory:
    def create_grid(self, argument: str) -> Grid:
        return ListBasedGrid(ALPHABET, ALPHABET)

    def get_name() -> str:
        return ALPHABET_GRID_NAME

options = [SquareRecursiveDivisionGridFactory, AlphabetGridFactory]

class GridFactoryOptions:
    def __init__(self, options: List[GridFactory]):
        self.options = {option.get_name():option for option in options}
    
    def get_option_names(self) -> List[str]:
        return self.options.keys()

    def create_grid(self, factory_name: str, arguments: str) -> Grid:
        return self.options[factory_name].create_grid(arguments)

grid_factory_options = GridFactoryOptions(options)

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_get_grid_factory_options() -> List[str]:
        '''Returns the mouse control chicken grid options'''
        return grid_factory_options.get_option_names()
    
    def mouse_control_chicken_create_grid_from_factory(factory: str, argument: str) -> Grid:
        '''Creates the specified mouse control chicken grid using the specified factory'''
        return grid_factory_options.create_grid(factory, argument)