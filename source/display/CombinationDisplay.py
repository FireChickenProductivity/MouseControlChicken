from ..grid.Grid import Grid
from .Display import Display, compute_boundaries_touching
from ..grid.Grid import RecursivelyDivisibleGridCombination, Rectangle
from ..grid.GridCalculations import compute_sub_grids, compute_grid_tree, apply_function_to_grid_tree_nodes_with_depth_based_state, Node
from typing import List, Type

class CombinationDisplay(Display):
    def __init__(self, primary_display: Display, secondary_display_types: List[Type]):
        self.primary_display = primary_display
        self.secondary_display_types = secondary_display_types
        self.rectangle: Rectangle = None
        self.secondary_displays = []
    
    def set_rectangle(self, rectangle: Rectangle):
        self.rectangle = rectangle
    
    def _setup_secondary_display_for_coordinate(self, tree: Node, index: int, coordinate: str):
        primary = tree.get_value()
        for child in tree.get_children():
            secondary = child.get_value()
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

    def _setup_secondary_displays_for_tree(self, tree: Node, index: int = 0):
        if index >= len(self.secondary_display_types) or not tree.has_children():
            return
        if len(tree.get_children()) == 1:
            for coordinate in tree.get_value().get_coordinate_system().get_primary_coordinates():
                self._setup_secondary_display_for_coordinate(tree, index, coordinate)
            self._setup_secondary_displays_for_tree(tree.get_children()[0], index + 1)
        else:
            for child in tree.get_children():
                self._setup_secondary_displays_for_tree(child, index)

    def _setup_secondary_displays_with_rectangle(self, grid: RecursivelyDivisibleGridCombination):
        tree = compute_grid_tree(grid)
        self._setup_secondary_displays_for_tree(tree)

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