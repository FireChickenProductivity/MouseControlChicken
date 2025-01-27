from .Display import *
from .UniversalDisplays import *
from .RectangularGridDisplays import *
from .CombinationDisplay import CombinationDisplay
from .NarrowDisplays import *
from .ReverseCoordinateDoublingDisplay import ReverseCoordinateDoublingDisplay
from ..grid.Grid import Grid, RecursivelyDivisibleGridCombination
from ..grid.GridCalculations import compute_sub_grids
from .WrappingDisplayType import WrappingDisplayType
from typing import List, Tuple, Type

class CombinationDisplayNotSupportedException(Exception):
    pass

DISPLAY_TYPES = [EmptyDisplay, RectangularGridFrameDisplay, UniversalPositionDisplay, DoubleFrameDisplay, QuadrupleFrameDisplay, NarrowDisplay, DoubleNarrowDisplay, RectangularPositionDisplay,
                 RectangularCheckerDisplay, RectangularDiagonalDisplay, DoubleRectangularDiagonalDisplay, QuadrupleRectangularDiagonalDisplay, ProximityFrameDisplay]
DISPLAY_WRAPPER_TYPES = [ReverseCoordinateDoublingDisplay]

def obtain_wrapper_and_wrapped_type_from(name: str) -> Tuple[Type, Type]:
    for wrapper_type in DISPLAY_WRAPPER_TYPES:
        typename = wrapper_type(EmptyDisplay).__class__.__name__
        wrapped_name_start = typename + "("
        if name.startswith(wrapped_name_start) and name.endswith(")"):
            return wrapper_type, obtain_display_type_from_name(name[len(wrapped_name_start):-1])
    raise ValueError(f"Could not find wrapper and wrapped type from name {name}")
        
def is_wrapped_name(name: str) -> bool:
    return "(" in name and name.endswith(")")

def obtain_wrap_type(name: str):
    wrapper_type, wrapped_type = obtain_wrapper_and_wrapped_type_from(name)
    resulting_type = WrappingDisplayType(wrapper_type, wrapped_type)
    return resulting_type

def obtain_simple_display_type_from_name(name: str) -> Type:
    for display_type in DISPLAY_TYPES:
        if display_type.get_name() == name:
            return display_type
    raise ValueError(f"Could not find display type with name {name} in {[display_type.get_name() for display_type in DISPLAY_TYPES]}")
    
def obtain_display_type_from_name(name: str) -> type:
    display_type = None
    if is_wrapped_name(name):
        display_type = obtain_wrap_type(name)
    else:
        display_type = obtain_simple_display_type_from_name(name)
    return display_type

DISPLAY_NAME_SEPARATOR = ":"

def is_combination_option_display_name(name: str) -> bool:
    return DISPLAY_NAME_SEPARATOR in name

class DisplayOption:
    def __init__(self, display_type: type):
        self.display_type = display_type
    
    def instantiate(self) -> Display:
        return self.display_type()

    def get_type(self):
        return self.display_type

    def get_types(self):
        return [self.get_type()]

    def get_name(self):
        return self.display_type.get_name()

    def is_partial_combination_option(self) -> bool:
        return False

    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return self.get_name()

class PartialCombinationDisplayOption(DisplayOption):
    SEPARATOR = "|"
    def __init__(self, display_type: type, index: int):
        self.display_type = display_type
        self.index = index
    
    def get_type(self):
        return self.display_type

    def get_name(self):
        return f"{self.index + 1}{PartialCombinationDisplayOption.SEPARATOR}{self.display_type.get_name()}"

    def get_display_name(self):
        return self.display_type.get_name()

    def is_partial_combination_option(self) -> bool:
        return True
    
    def get_index(self):
        return self.index

    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return self.get_name()
    
class CombinationDisplayOption:
    def __init__(self, display_types: List[type]):
        self.display_types = display_types
    
    def instantiate(self) -> CombinationDisplay:
        primary = self.display_types[0]()
        secondary = self.display_types[1:]
        return CombinationDisplay(primary, secondary)
    
    def set_display(self, display: Display, index: int):
        if index < len(self.display_types):
            self.display_types[index] = display
        elif index == len(self.display_types):
            self.display_types.append(display)
        else:
            raise ValueError(f"Index {index} is too large for Combination Display Option display types {self.display_types}")

    def receive_partial_combination_display_option(self, option: PartialCombinationDisplayOption):
        self.set_display(option.get_type(), option.get_index())

    def get_types(self):
        return self.display_types

    def get_name(self):
        return ":".join([display_type.get_name() for display_type in self.display_types])

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.get_name()

class DisplayOptions:
    def __init__(self, options: List[DisplayOption], *, is_for_combination_grid: bool = False):
        self.options = {}
        for option in options: self.options[option.get_name()] = option
        self.is_for_combination_grid = is_for_combination_grid

    def get_names(self) -> List[str]:
        return self.options.keys()
    
    def create_display_from_option(self, name: str, current_display: Display = None) -> Display:
        if self.is_for_combination_grid:
            option = self.create_combination_display_option_from_option(name, current_display)
            display = option.instantiate()
        else:
            if name not in self.options: raise ValueError(f"Name {name} not in options {self.options.keys()}")
            option = self.options[name]
            display = option.instantiate()
        return display, option

    def create_combination_display_option_from_option(self, name: str, current_display: Display = None):
        if is_combination_option_display_name(name):
            return self.create_combination_display_option_from_name(name)
        partial_option = self.compute_partial_option_from_name(name)
        sub_display_names = []
        if current_display:
            sub_display_names = current_display.get_name().split(DISPLAY_NAME_SEPARATOR)
        else:
            sub_display_names = ["Empty"]*(partial_option.get_index() + 1)
        combination = self.create_combination_display_option_from_sub_displays(sub_display_names)
        combination.receive_partial_combination_display_option(partial_option)
        return combination

    def create_combination_display_option_from_name(self, name: str) -> CombinationDisplay:
        sub_display_names = name.split(DISPLAY_NAME_SEPARATOR)
        return self.create_combination_display_option_from_sub_displays(sub_display_names)

    def create_combination_display_option_from_sub_displays(self, sub_display_names: List[str]) -> CombinationDisplay:
        sub_displays = [obtain_display_type_from_name(displayname) for displayname in sub_display_names]
        combination = CombinationDisplayOption(sub_displays)
        return combination

    def compute_partial_option_from_name(self, name: str) -> PartialCombinationDisplayOption:
        if PartialCombinationDisplayOption.SEPARATOR in name:
            order_number, display_name = name.split(PartialCombinationDisplayOption.SEPARATOR)
        else:
            order_number = 1
            display_name = name
        normalized_option_name = str(order_number) + PartialCombinationDisplayOption.SEPARATOR + display_name
        return self.options[normalized_option_name]

    def get_option_with_name(self, name: str) -> DisplayOption:
        return self.options[name]

def compute_display_option_types_given_singular_grid(grid: Grid) -> List[type]:
    if grid.is_wrapper():
        if grid.is_doubling():
            return [WrappingDisplayType(ReverseCoordinateDoublingDisplay, display_type) for display_type in compute_display_option_types_given_singular_grid(grid.get_primary_grid())]
        grid = grid.get_wrapped_grid()
    types = [display_type for display_type in DISPLAY_TYPES if display_type.supports_grid(grid)]
    return types

def compute_display_options_given_singular_grid(grid: Grid) -> DisplayOptions:
    types = compute_display_option_types_given_singular_grid(grid)
    options = DisplayOptions([DisplayOption(display_type) for display_type in types])
    return options

def compute_partial_display_options_for_grid(sub_grid: Grid, index: int) -> List[PartialCombinationDisplayOption]:
    options = [ PartialCombinationDisplayOption(display_type, index) 
                    for display_type in compute_display_option_types_given_singular_grid(sub_grid)
    ]
    return options

def compute_combination_display_options_given_grid(grid: RecursivelyDivisibleGridCombination) -> DisplayOptions:
    '''This will return the partial display options for every sub grid.'''
    options = []
    sub_grids = compute_sub_grids(grid)
    for index, sub_grid in enumerate(sub_grids):
        new_options = compute_partial_display_options_for_grid(sub_grid, index)
        options.extend(new_options)
        if not should_consider_sub_grids_after_grid(sub_grid):
            break
    return DisplayOptions(options, is_for_combination_grid=True)

def separate_combination_display_options_by_index(options: DisplayOptions) -> List[List[PartialCombinationDisplayOption]]:
    separated = []
    for name in options.get_names():
        option = options.compute_partial_option_from_name(name)
        index = option.get_index()
        while len(separated) <= index:
            separated.append([])
        separated[index].append(option)
    return separated

def compute_display_options_separated_by_index_for_grid(grid: RecursivelyDivisibleGridCombination) -> List[List[PartialCombinationDisplayOption]]:
    if not should_compute_combination_display_options_for_grid(grid):
        raise CombinationDisplayNotSupportedException(str(grid))
    options = compute_combination_display_options_given_grid(grid)
    return separate_combination_display_options_by_index(options)

def should_consider_sub_grids_after_grid(grid: Grid) -> bool:
    if grid.is_wrapper():
        grid = grid.get_wrapped_grid()
    return grid.has_nonoverlapping_sub_rectangles()

def should_compute_combination_display_options_for_grid(grid: Grid) -> bool:
    return grid.is_combination() and should_consider_sub_grids_after_grid(grid) or (grid.is_doubling() and should_compute_combination_display_options_for_grid(grid.get_primary_grid()))

def compute_display_options_given_grid(grid: Grid) -> DisplayOptions:
    options = None
    if should_compute_combination_display_options_for_grid(grid):
        options = compute_combination_display_options_given_grid(grid)
    else:
        options = compute_display_options_given_singular_grid(grid)
    return options

def compute_display_option_names_given_options(options: DisplayOptions) -> List[str]:
    return [option for option in options.get_names()]

def compute_display_options_names_given_grid(grid: Grid) -> List[str]:
    display_options = compute_display_options_given_grid(grid)
    options_text = compute_display_option_names_given_options(display_options)
    return options_text

def create_display_option(types: List[type]) -> DisplayOption:
    if len(types) == 1:
        return DisplayOption(types[0])
    return CombinationDisplayOption(types)

def compute_combined_display_option(non_combination_display_option: DisplayOption, old: DisplayOption) -> DisplayOption:
    combination = CombinationDisplayOption(non_combination_display_option.get_types() + old.get_types())
    return combination

def is_first_type_wrapped(types):
    return isinstance(types[0], WrappingDisplayType)

def unwrap_first_type(types):
    wrapped_type = types[0].get_wrapped()
    types[0] = wrapped_type

def remove_first_display_type(types):
    types.pop(0)
    if len(types) == 0:
        types.append(EmptyDisplay)

def remove_first_display_option(display_option: DisplayOption) -> DisplayOption:
    types = display_option.get_types()[:]
    if is_first_type_wrapped(types):
        unwrap_first_type(types)
    else:
        remove_first_display_type(types)
    return create_display_option(types)

def _compute_reverse_coordinate_doubling_display_type_from_type(display_type: type) -> type:
    if isinstance(display_type, WrappingDisplayType):
        wrapped = display_type.get_wrapped()
        return WrappingDisplayType(ReverseCoordinateDoublingDisplay, wrapped)
    return WrappingDisplayType(ReverseCoordinateDoublingDisplay, display_type)

def wrap_first_display_option_with_doubling(display_option: DisplayOption) -> DisplayOption:
    types = display_option.get_types()[:]
    types[0] = _compute_reverse_coordinate_doubling_display_type_from_type(types[0])
    return create_display_option(types)
