from .Display import *
from .UniversalDisplays import *
from .RectangularGridDisplays import *
from .NarrowDisplay import *
from .Grid import Grid
from typing import List

display_types = [RectangularGridFrameDisplay, UniversalPositionDisplay, DoubleFrameDisplay, QuadrupleFrameDisplay, NarrowDisplay]

class DisplayOption:
    def __init__(self, display_type: type):
        self.display_type = display_type
    
    def instantiate(self) -> Display:
        return self.display_type()

    def get_name(self):
        return self.display_type.get_name()

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

class DisplayOptionComputer:
    def compute_display_options(self, grid: Grid) -> DisplayOptions:
        options = DisplayOptions([DisplayOption(display_type) for display_type in display_types if display_type.supports_grid(grid)])
        return options