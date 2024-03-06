from .Display import *
from .UniversalDisplays import *
from .RectangularGridDisplays import *
from .CombinationDisplay import CombinationDisplay
from .NarrowDisplays import *
from ..grid.Grid import Grid, compute_sub_grids, RecursivelyDivisibleGridCombination
from typing import List

display_types = [RectangularGridFrameDisplay, UniversalPositionDisplay, DoubleFrameDisplay, QuadrupleFrameDisplay, NarrowDisplay, DoubleNarrowDisplay, RectangularPositionDisplay,
                 RectangularCheckerDisplay]

class DisplayOption:
    def __init__(self, display_type: type):
        self.display_type = display_type
    
    def instantiate(self) -> Display:
        return self.display_type()

    def get_type(self):
        return self.display_type

    def get_name(self):
        return self.display_type.get_name()

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

    def get_types(self):
        return self.display_types

    def get_name(self):
        return ":".join([display_type.get_name() for display_type in self.display_types])

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.get_name()

class DisplayOptions:
    def __init__(self, options: List[DisplayOption]):
        self.options = {}
        for option in options: self.options[option.get_name()] = option

    def get_names(self) -> List[str]:
        return self.options.keys()
    
    def create_display_from_option(self, name: str):
        return self.options[name].instantiate()

def compute_display_option_types_given_singular_grid(grid: Grid) -> List[type]:
    types = [display_type for display_type in display_types if display_type.supports_grid(grid)]
    return types

def compute_display_options_given_singular_grid(grid: Grid) -> DisplayOptions:
    types = compute_display_option_types_given_singular_grid(grid)
    options = DisplayOptions([DisplayOption(display_type) for display_type in types])
    return options

def compute_combination_display_options_given_grid(grid: RecursivelyDivisibleGridCombination) -> DisplayOptions:
    '''This function will return all possible valid combinations of displays for the grid.
        A valid combination of displays has at most the number of sub grids as the number of displays with each display being valid for
        the corresponding sub grid.'''
    options = []
    sub_grids = compute_sub_grids(grid)
    for sub_grid in sub_grids:
        types_for_sub_grid = compute_display_option_types_given_singular_grid(sub_grid)
        previous_level_options = options[:]
        if previous_level_options:
            for option in previous_level_options:
                for display_type in types_for_sub_grid:
                    new_option = CombinationDisplayOption(option.get_types() + [display_type])
                    options.append(new_option)
        else:
            for display_type in types_for_sub_grid:
                new_option = CombinationDisplayOption([display_type])
                options.append(new_option)
    return DisplayOptions(options)

def compute_display_options_given_grid(grid: Grid) -> DisplayOptions:
    if grid.is_combination():
        return compute_combination_display_options_given_grid(grid)
    else:
        return compute_display_options_given_singular_grid(grid)

def compute_display_options_names_given_grid(grid: Grid) -> List[str]:
    display_options = compute_display_options_given_grid(grid)
    options_text = [option for option in display_options.get_names()]
    return options_text

def create_display_given_name_and_grid(name: str, grid: Grid) -> Display:
    options = compute_display_options_given_grid(grid)
    return options.create_display_from_option(name)
