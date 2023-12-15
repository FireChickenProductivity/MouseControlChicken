from .Display import *
from .UniversalDisplays import *
from .RectangularGridDisplays import *
from .Grid import Grid

display_types = [RectangularGridFrameDisplay, UniversalPositionDisplay]

class DisplayOptionComputer:
    def compute_display_options(self, grid: Grid):
        return [display_type for display_type in display_types if display_type.supports_grid(grid)]