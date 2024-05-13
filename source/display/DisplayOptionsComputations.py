from .Display import *
from .UniversalDisplays import *
from .RectangularGridDisplays import *
from .CombinationDisplay import CombinationDisplay
from .NarrowDisplays import *
from ..grid.Grid import Grid, compute_sub_grids, RecursivelyDivisibleGridCombination
from typing import List

display_types = [EmptyDisplay, RectangularGridFrameDisplay, UniversalPositionDisplay, DoubleFrameDisplay, QuadrupleFrameDisplay, NarrowDisplay, DoubleNarrowDisplay, RectangularPositionDisplay,
                 RectangularCheckerDisplay]

def obtain_display_type_from_name(name: str) -> type:
    for display_type in display_types:
        if display_type.get_name() == name:
            return display_type
    raise ValueError(f"Could not find display type with name {name} in {[display_type.get_name() for display_type in display_types]}")

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
            display = self.create_combination_display_from_option(name, current_display)
        else:
            display = self.options[name].instantiate()
        return display

    def create_combination_display_from_option(self, name: str, current_display: Display = None) -> CombinationDisplay:
        if is_combination_option_display_name(name):
            return self.create_combination_display_option_from_name(name).instantiate()
        partial_option = self.compute_partial_option_from_name(name)
        sub_display_names = []
        if current_display:
            sub_display_names = current_display.get_name().split(DISPLAY_NAME_SEPARATOR)
        else:
            sub_display_names = ["Empty"]*(partial_option.get_index() + 1)
        combination = self.create_combination_display_option_from_sub_displays(sub_display_names)
        combination.receive_partial_combination_display_option(partial_option)
        return combination.instantiate()

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

def compute_display_option_types_given_singular_grid(grid: Grid) -> List[type]:
    types = [display_type for display_type in display_types if display_type.supports_grid(grid)]
    return types

def compute_display_options_given_singular_grid(grid: Grid) -> DisplayOptions:
    types = compute_display_option_types_given_singular_grid(grid)
    options = DisplayOptions([DisplayOption(display_type) for display_type in types])
    return options

def compute_combination_display_options_given_grid(grid: RecursivelyDivisibleGridCombination) -> DisplayOptions:
    '''This will return the partial display options for every sub grid.'''
    options = []
    sub_grids = compute_sub_grids(grid)
    for index, sub_grid in enumerate(sub_grids):
        options += [
            PartialCombinationDisplayOption(display_type, index) 
            for display_type in compute_display_option_types_given_singular_grid(sub_grid)
        ]
    return DisplayOptions(options, is_for_combination_grid=True)

def compute_display_options_given_grid(grid: Grid) -> DisplayOptions:
    if grid.is_combination() and grid.has_nonoverlapping_sub_rectangles():
        print('combination')
        return compute_combination_display_options_given_grid(grid)
    else:
        print('singular')
        return compute_display_options_given_singular_grid(grid)

def compute_display_options_names_given_grid(grid: Grid) -> List[str]:
    display_options = compute_display_options_given_grid(grid)
    options_text = [option for option in display_options.get_names()]
    return options_text

def create_display_given_name_and_grid(name: str, grid: Grid) -> Display:
    options = compute_display_options_given_grid(grid)
    return options.create_display_from_option(name)
