from source.Grid import Grid
from .Display import Display
from ..Grid import RecursivelyDivisibleGridCombination, Rectangle, compute_sub_grids
from typing import List, Callable

class CombinationDisplay(Display):
    def __init__(self, primary_display: Display, secondary_display_creation_functions: List[Callable[[], Display]]):
        self.primary_display = primary_display
        self.secondary_display_creation_functions = secondary_display_creation_functions
        self.rectangle: Rectangle = None
        self.secondary_displays = []
    
    def set_rectangle(self, rectangle: Rectangle):
        self.primary_display.set_rectangle(rectangle)
        self.rectangle = rectangle
    
    def set_grid(self, grid: RecursivelyDivisibleGridCombination):
        self.grid = grid
        self.hide()
        grids = compute_sub_grids(grid)
        self.secondary_displays = []
        self.primary_display.set_grid(grid)
        if self.rectangle:
            self.set_rectangle(self.rectangle)
            for index, sub_grid in enumerate(grids):
                if sub_grid.is_combination():
                    for coordinate in sub_grid.get_coordinate_system().get_coordinates():
                        sub_rectangle = sub_grid.compute_sub_rectangle_for(coordinate)
                        sub_display = self.secondary_display_creation_functions[index]()
                        sub_display.set_rectangle(sub_rectangle)
                        self.secondary_displays.append(sub_display)

    def show(self):
        self.primary_display.show()
        for display in self.secondary_displays:
            display.show()

    def hide(self):
        self.primary_display.hide()
        for display in self.secondary_displays:
            display.hide()
        
    def refresh(self):
        self.primary_display.refresh()
        for display in self.secondary_displays:
            display.refresh()
        
    @staticmethod
    def supports_grid(grid: Grid) -> bool:
        return grid.is_combination()
        
    