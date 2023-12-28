from .Grid import Grid, RecursivelyDivisibleGridCombination
from .GridOptions import GridOptions
from .RecursiveDivisionGrid import SquareRecursiveDivisionGrid
from .RectangularGrid import ListBasedGrid
from .TagManagement import GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG, GRID_CREATION_ARGUMENT_GRID_OPTION_TAG
from typing import List
from talon import Module, actions

ONE_TO_NINE_GRID_NAME = "one to nine division"
ALPHABET_GRID_NAME = "Alphabet"
DOUBLE_ALPHABET_GRID_NAME = "Double Alphabet"
RECURSIVELY_DIVISIBLE_GRID_COMBINATION_NAME = "Recursively Divisible Combination"

ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ]
DOUBLE_ALPHABET = ALPHABET + ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", ]

GRID_ARGUMENT_SEPARATOR = ":"

class OptionsNotSupportedException(Exception): pass

class FactoryArgumentType:
    def __init__(self, type: type, tag: str):
        self.type = type
        self.tag = tag
    
    def does_argument_match_type(self, argument):
        return isinstance(argument, self.type) and self._argument_has_valid_value(argument)
    
    def _argument_has_valid_value(self, argument):
        pass

    def get_tag(self) -> str:
        return self.tag

    def supports_options_display(self) -> bool:
        return False

    def get_options(self) -> List[str]:
        raise OptionsNotSupportedException()

class TwoToNineArgumentType(FactoryArgumentType):
    def __init__(self):
        super().__init__(int, GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG)
    
    def _argument_has_valid_value(self, argument):
        return argument >= 2 and argument <= 9
    
class GridOptionArgumentType(FactoryArgumentType):
    def __init__(self):
        super().__init__(str, GRID_CREATION_ARGUMENT_GRID_OPTION_TAG)

    def _argument_has_valid_value(self, argument):
        options: self.get_options()
        return options.has_option(argument)

    def supports_options_display(self) -> bool:
        return True

    def get_options(self) -> List[str]:
        options: GridOptions = actions.user.mouse_control_chicken_get_grid_options()
        return options.get_option_names()

class GridFactory:
    def create_grid(self, argument: str) -> Grid:
        pass

    def get_name(self) -> str:
        pass

    def matches_option(self, option: str) -> bool:
        return option == self.get_name()
    
    def get_arguments_description(self) -> str:
        return ""

    def get_argument_types(self) -> List[FactoryArgumentType]:
        return []

class SquareRecursiveDivisionGridFactory(GridFactory):
    def create_grid(self, argument: str) -> Grid:
        argument = int(argument)
        return SquareRecursiveDivisionGrid(argument)

    def get_name(self) -> str:
        return "Square Recursive Division Grid"
    
    def get_arguments_description(self) -> str:
        return "A single integer. That integer squared gives the number of times to divide the rectangle."

    def get_argument_types(self) -> List[FactoryArgumentType]:
        return [TwoToNineArgumentType()]


class AlphabetGridFactory(GridFactory):
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
        options = argument.split(GRID_ARGUMENT_SEPARATOR)
        primary = create_grid_from_options(options[0]) 
        secondary = create_grid_from_options(options[1])
        combination = RecursivelyDivisibleGridCombination(primary, secondary)
        return combination

    def get_name(self) -> str:
        return RECURSIVELY_DIVISIBLE_GRID_COMBINATION_NAME
    
    def get_arguments_description(self) -> str:
        return "(grid option one) (grid option two)"

    def get_argument_types(self) -> List[FactoryArgumentType]:
        return [GridOptionArgumentType(), GridOptionArgumentType()]

options = [SquareRecursiveDivisionGridFactory(), AlphabetGridFactory(), DoubleAlphabetGridFactory(), RecursivelyDivisibleGridCombinationGridFactory()]

class GridFactoryOptions:
    def __init__(self, options: List[GridFactory]):
        self.options = {option.get_name():option for option in options}
    
    def get_option_names(self) -> List[str]:
        return self.options.keys()

    def create_grid(self, factory_name: str, arguments: str) -> Grid:
        return self.options[factory_name].create_grid(arguments)
    
    def get_factory(self, factory_name: str) -> GridFactory:
        return self.options[factory_name]

grid_factory_options = GridFactoryOptions(options)

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_get_grid_factory_options() -> List[str]:
        '''Returns the mouse control chicken grid options'''
        names = [name for name in grid_factory_options.get_option_names()]
        return names
    
    def mouse_control_chicken_create_grid_from_factory(factory: str, argument: str) -> Grid:
        '''Creates the specified mouse control chicken grid using the specified factory'''
        return grid_factory_options.create_grid(factory, argument)

    def mouse_control_chicken_create_grid_from_options(name: str) -> Grid:
        '''Creates the specified mouse control chicken grid using the specified option name'''
        return create_grid_from_options(name)

    def mouse_control_chicken_get_grid_factory(name: str) -> GridFactory:
        '''Returns the mouse control chicken grid factory with the specified name'''
        return grid_factory_options.get_factory(name)


def create_grid_from_options(name: str) -> Grid:
    options: GridOptions = actions.user.mouse_control_chicken_get_grid_options()
    option = options.get_option(name)
    grid = grid_factory_options.create_grid(option.get_factory_name(), option.get_argument())
    return grid