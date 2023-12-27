from .Grid import Grid, RecursivelyDivisibleGridCombination
from .GridOptions import GridOptions
from .RecursiveDivisionGrid import SquareRecursiveDivisionGrid
from .RectangularGrid import ListBasedGrid
from typing import List
from talon import Module, actions

ONE_TO_NINE_GRID_NAME = "one to nine division"
ALPHABET_GRID_NAME = "Alphabet"
DOUBLE_ALPHABET_GRID_NAME = "Double Alphabet"
RECURSIVELY_DIVISIBLE_GRID_COMBINATION_NAME = "Recursively Divisible Combination"

ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ]
DOUBLE_ALPHABET = ALPHABET + ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", ]

class GridFactory:
    def create_grid(self, argument: str) -> Grid:
        pass

    def get_name(self) -> str:
        pass

    def matches_option(self, option: str) -> bool:
        return option == self.get_name()
    
    def get_arguments_description(self) -> str:
        return ""

    def get_argument_types(self) -> List:
        return []

class SquareRecursiveDivisionGridFactory:
    def create_grid(self, argument: str) -> Grid:
        argument = int(argument)
        return SquareRecursiveDivisionGrid(argument)

    def get_name(self) -> str:
        return "Square Recursive Division Grid"
    
    def get_arguments_description(self) -> str:
        return "A single integer. That integer squared gives the number of times to divide the rectangle."


class AlphabetGridFactory:
    def create_grid(self, argument: str) -> Grid:
        return ListBasedGrid(ALPHABET, ALPHABET)

    def get_name(self) -> str:
        return ALPHABET_GRID_NAME
    
class DoubleAlphabetGridFactory:
    def create_grid(self, argument: str) -> Grid:
        return ListBasedGrid(DOUBLE_ALPHABET, DOUBLE_ALPHABET)

    def get_name(self) -> str:
        return DOUBLE_ALPHABET_GRID_NAME

class RecursivelyDivisibleGridCombinationGridFactory:
    def create_grid(self, argument: str) -> Grid:
        options = argument.split(":")
        primary = create_grid_from_options(options[0]) 
        secondary = create_grid_from_options(options[1])
        combination = RecursivelyDivisibleGridCombination(primary, secondary)
        return combination

    def get_name(self) -> str:
        return RECURSIVELY_DIVISIBLE_GRID_COMBINATION_NAME
    
    def get_arguments_description(self) -> str:
        return "(grid option one) (grid option two)"

options = [SquareRecursiveDivisionGridFactory(), AlphabetGridFactory(), DoubleAlphabetGridFactory(), RecursivelyDivisibleGridCombinationGridFactory()]

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

    def mouse_control_chicken_create_grid_from_options(name: str) -> Grid:
        '''Creates the specified mouse control chicken grid using the specified option name'''
        return create_grid_from_options(name)


def create_grid_from_options(name: str) -> Grid:
    options: GridOptions = actions.user.mouse_control_chicken_get_grid_options()
    option = options.get_option(name)
    grid = grid_factory_options.create_grid(option.get_factory_name(), option.get_argument())
    return grid