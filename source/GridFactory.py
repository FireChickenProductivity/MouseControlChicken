from .grid.Grid import Grid, RecursivelyDivisibleGridCombination
from .GridOptionsList import get_grid_options
from .GridOptions import GridOptions
from .grid.RecursiveDivisionGrid import RectangularRecursiveDivisionGrid, RectangularDivisionAmounts
from .grid.RectangularGrid import ListBasedGrid
from .grid.SingleLayerFromRecursiveGridGrid import SingleLayerFromRecursiveGridGrid
from .grid.ReverseCoordinateDoublingGrid import ReverseCoordinateHorizontalDoublingGrid, ReverseCoordinateVerticalDoublingGrid
from .GridFactoryArgumentTypes import FactoryArgumentType, TwoToNineArgumentType, GridOptionArgumentType, PositiveIntegerArgumentType, InvalidFactoryArgumentException
from typing import List
from talon import Module, actions

ONE_TO_NINE_GRID_NAME = "one to nine division"
ALPHABET_GRID_NAME = "Alphabet"
DOUBLE_ALPHABET_GRID_NAME = "Double Alphabet"
RECURSIVELY_DIVISIBLE_GRID_COMBINATION_NAME = "Recursively Divisible Combination"
HORIZONTAL_DOUBLING_GRID_NAME = "Horizontal Doubling"
VERTICAL_DOUBLING_GRID_NAME = "Vertical Doubling"

ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ]
DOUBLE_ALPHABET = ALPHABET + ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", ]

GRID_ARGUMENT_SEPARATOR = ":"

class GridFactory:
    def create_grid(self, argument: str) -> Grid:
        components = self._compute_argument_components(argument)
        if self._are_argument_components_valid(components):
            return self._create_grid_with_valid_arguments_from_components_in_string_form(components)
        else:
            raise InvalidFactoryArgumentException()

    def _compute_argument_components(self, argument: str) -> List[str]:
        return argument.split(GRID_ARGUMENT_SEPARATOR)

    def _are_argument_components_valid(self, components: List[str]) -> bool:
        argument_types = self.get_argument_types()
        if len(argument_types) == 0:
            return len(components) == 1 and components[0] == ""
        if len(components) != len(argument_types):
            return False
        for index in range(len(components)):
            if not argument_types[index].does_argument_match_type(components[index]):
                return False
        return True
    
    def _create_grid_with_valid_arguments_from_components_in_string_form(self, components: List[str]) -> Grid:
        converted_components = self._convert_arguments(components)
        return self.create_grid_with_valid_argument_from_components(converted_components)

    def _convert_arguments(self, components: List[str]) -> List[object]:
        argument_types = self.get_argument_types()
        return [argument_types[index].convert_argument(components[index]) for index in range(len(argument_types))]

    def create_grid_with_valid_argument_from_components(self, components: List[str]) -> Grid:
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
    def create_grid_with_valid_argument_from_components(self, components: List[str]) -> Grid:
        argument = int(components[0])
        input_coordinate_list = [str(index + 1) for index in range(argument**2)]
        return RectangularRecursiveDivisionGrid(RectangularDivisionAmounts(argument, argument), input_coordinate_list)

    def get_name(self) -> str:
        return "Square Recursive Division Grid"
    
    def get_arguments_description(self) -> str:
        return "A single integer. That integer squared gives the number of times to divide the rectangle."

    def get_argument_types(self) -> List[FactoryArgumentType]:
        return [TwoToNineArgumentType()]

class RectangularRecursiveDivisionGridFactory(GridFactory):
    def create_grid_with_valid_argument_from_components(self, components: List[str]) -> Grid:
        horizontal = int(components[0])
        vertical = int(components[1])
        input_coordinate_list = [str(index + 1) for index in range(horizontal * vertical)]
        return RectangularRecursiveDivisionGrid(RectangularDivisionAmounts(horizontal, vertical), input_coordinate_list)

    def get_name(self) -> str:
        return "Rectangular Recursive Division Grid"
    
    def get_arguments_description(self) -> str:
        return "Two integers. The first integer is the number of horizontal divisions. The second integer is the number of vertical divisions. "

    def get_argument_types(self) -> List[FactoryArgumentType]:
        return [PositiveIntegerArgumentType(), PositiveIntegerArgumentType()]

class AlphabetGridFactory(GridFactory):
    def create_grid_with_valid_argument_from_components(self, components: List[str]) -> Grid:
        return ListBasedGrid(ALPHABET, ALPHABET)

    def get_name(self) -> str:
        return ALPHABET_GRID_NAME
    
class DoubleAlphabetGridFactory(GridFactory):
    def create_grid_with_valid_argument_from_components(self, components: List[str]) -> Grid:
        return ListBasedGrid(DOUBLE_ALPHABET, DOUBLE_ALPHABET)

    def get_name(self) -> str:
        return DOUBLE_ALPHABET_GRID_NAME

class RecursivelyDivisibleGridCombinationGridFactory(GridFactory):
    def create_grid_with_valid_argument_from_components(self, components: List[str]) -> Grid:
        primary = create_grid_from_options(components[0]) 
        if primary.supports_narrowing():
            primary = SingleLayerFromRecursiveGridGrid(primary)
        secondary = create_grid_from_options(components[1])
        combination = RecursivelyDivisibleGridCombination(primary, secondary)
        return combination

    def get_name(self) -> str:
        return RECURSIVELY_DIVISIBLE_GRID_COMBINATION_NAME
    
    def get_arguments_description(self) -> str:
        return "(grid option one) (grid option two)"

    def get_argument_types(self) -> List[FactoryArgumentType]:
        return [GridOptionArgumentType(), GridOptionArgumentType()]

class DoublingGridFactory(GridFactory):
    def get_arguments_description(self) -> str:
        return "(grid option)"

    def get_argument_types(self) -> List[FactoryArgumentType]:
        return [GridOptionArgumentType()]

class HorizontalDoublingGridFactory(DoublingGridFactory):
    def create_grid_with_valid_argument_from_components(self, components: List[str]) -> Grid:
        primary = create_grid_from_options(components[0])
        return ReverseCoordinateHorizontalDoublingGrid(primary)
    
    def get_name(self) -> str:
        return HORIZONTAL_DOUBLING_GRID_NAME

class VerticalDoublingGridFactory(DoublingGridFactory):
    def create_grid_with_valid_argument_from_components(self, components: List[str]) -> Grid:
        primary = create_grid_from_options(components[0])
        return ReverseCoordinateVerticalDoublingGrid(primary)
    
    def get_name(self) -> str:
        return VERTICAL_DOUBLING_GRID_NAME

options = [
    SquareRecursiveDivisionGridFactory(),
    RectangularRecursiveDivisionGridFactory(),
    AlphabetGridFactory(),
    DoubleAlphabetGridFactory(),
    RecursivelyDivisibleGridCombinationGridFactory(),
    HorizontalDoublingGridFactory(),
    VerticalDoublingGridFactory()
]

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
    options: GridOptions = get_grid_options()
    option = options.get_option(name)
    grid = grid_factory_options.create_grid(option.get_factory_name(), option.get_argument())
    return grid