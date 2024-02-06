from ..Grid import Grid
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
        if self.grid and self.secondary_display_creation_functions:
            self._setup_secondary_displays(self.grid)
        print(self.grid)
    
    def _setup_secondary_display_for_coordinate(self, grids: List[RecursivelyDivisibleGridCombination], index: int, coordinate: str):
        primary = grids[index]
        secondary = grids[index + 1]
        sub_rectangle = primary.compute_sub_rectangle_for(coordinate)
        print('sub_rectangle', sub_rectangle)
        print('secondary', secondary)
        print('primary', primary)
        sub_display = self.secondary_display_creation_functions[index]()
        #Big problem is the secondary does not exist around any rectangles at this point probably
        #Might need to maintain a sub grid for each secondary display
        sub_display.set_grid(secondary)
        sub_display.set_rectangle(sub_rectangle)
        self.secondary_displays.append(sub_display)
        print('completed appending')

    def _setup_secondary_displays_for_grid(self, grids: List[RecursivelyDivisibleGridCombination], index: int):
        for coordinate in grids[0].get_coordinate_system().get_primary_coordinates():
            self._setup_secondary_display_for_coordinate(grids, index, coordinate)

    def _setup_secondary_displays_with_rectangle(self, grid: RecursivelyDivisibleGridCombination):
        grids = compute_sub_grids(grid)
        for index in range(len(self.secondary_display_creation_functions)):
            self._setup_secondary_displays_for_grid(grids, index)

    def _setup_secondary_displays(self, grid: RecursivelyDivisibleGridCombination):
        self.secondary_displays = []
        if self.rectangle:
            self._setup_secondary_displays_with_rectangle(grid)
                
    def set_grid(self, grid: RecursivelyDivisibleGridCombination):
        self.grid = grid
        self.hide()
        self.primary_display.set_grid(grid.get_primary_grid())
        

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
    
    def _displays_support_corresponding_sub_grid(self, grid: RecursivelyDivisibleGridCombination) -> bool:
        return self.primary_display.supports_grid(grid) and \
            all([display.supports_grid(sub_grid) for display, sub_grid in zip(self.secondary_displays, compute_sub_grids(grid)[1:])])
    
    def supports_grid(self, grid: Grid) -> bool:
        return grid.is_combination() and self._displays_support_corresponding_sub_grid(grid)
        
    def get_name(self) -> str:
        name = self.primary_display.get_name()
        for display in self.secondary_displays:
            name += ":" + display.get_name()
        return name