from ..grid.Grid import Grid
from .Display import Display, compute_boundaries_touching
from ..grid.Grid import RecursivelyDivisibleGridCombination, Rectangle
from ..grid.GridCalculations import compute_sub_grids
from typing import List, Type

class CombinationDisplay(Display):
    def __init__(self, primary_display: Display, secondary_display_types: List[Type]):
        self.primary_display = primary_display
        self.secondary_display_types = secondary_display_types
        self.rectangle: Rectangle = None
        self.secondary_displays = []
    
    def set_rectangle(self, rectangle: Rectangle):
        self.rectangle = rectangle
    
    def _compute_primary_grids(self, grid: RecursivelyDivisibleGridCombination) -> List[RecursivelyDivisibleGridCombination]:
        if grid.supports_reversed_coordinates() and grid.is_wrapper():
            result = [grid.get_primary_grid(), grid.get_secondary_grid()]
        else:
            result = [grid]
        return result

    def _setup_secondary_display_for_coordinate(self, grids: List[RecursivelyDivisibleGridCombination], index: int, coordinate: str):
        primary_grids = self._compute_primary_grids(grids[0])
        secondary = grids[index + 1]
        for primary in primary_grids:
            sub_rectangle = primary.compute_sub_rectangle_for(coordinate)
            secondary.make_around(sub_rectangle)
            sub_display = self.secondary_display_types[index]()
            sub_display.set_grid(secondary)
            sub_display.set_rectangle(sub_rectangle)
            if sub_display.is_boundary_acknowledging():
                boundaries_touching = compute_boundaries_touching(sub_rectangle, primary.get_rectangle())
                sub_display.draw_on_canvas_given_boundaries_touching(self.canvas, boundaries_touching)
            else:
                sub_display.draw_on(self.canvas)
            self.secondary_displays.append(sub_display)

    def _setup_secondary_displays_for_grid(self, grids: List[RecursivelyDivisibleGridCombination], index: int):
        for coordinate in grids[0].get_coordinate_system().get_primary_coordinates():
            self._setup_secondary_display_for_coordinate(grids, index, coordinate)

    def _setup_secondary_displays_with_rectangle(self, grid: RecursivelyDivisibleGridCombination):
        grids = compute_sub_grids(grid)
        for index in range(len(self.secondary_display_types)):
            self._setup_secondary_displays_for_grid(grids, index)

    def _setup_secondary_displays(self, grid: RecursivelyDivisibleGridCombination):
        self.secondary_displays = []
        if self.rectangle:
            self._setup_secondary_displays_with_rectangle(grid)
                
    def set_grid(self, grid: RecursivelyDivisibleGridCombination):
        self.grid = grid
    
    def draw_on(self, canvas):
        self.primary_display.set_grid(self.grid)
        self.primary_display.set_rectangle(self.rectangle)
        self.primary_display.draw_on(canvas)
        self.canvas = canvas
        self._setup_secondary_displays(self.grid)

    def _displays_support_corresponding_sub_grid(self, grid: RecursivelyDivisibleGridCombination) -> bool:
        return self.primary_display.supports_grid(grid) and \
            all([display.supports_grid(sub_grid) for display, sub_grid in zip(self.secondary_displays, compute_sub_grids(grid)[1:])])
    
    def supports_grid(self, grid: Grid) -> bool:
        return grid.is_combination() and self._displays_support_corresponding_sub_grid(grid)
        
    def get_name(self) -> str:
        name = self.primary_display.get_name()
        for display_type in self.secondary_display_types:
            name += ":" + display_type.get_name()
        return name