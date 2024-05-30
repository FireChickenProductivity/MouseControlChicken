from .Display import Display, compute_boundaries_touching
from copy import deepcopy
from ..grid.ReverseCoordinateDoublingGrid import ReverseCoordinateDoublingGrid
from ..grid.Grid import Grid
from ..grid.GridCalculations import find_first_grid_tree_node_matching_function, GridNotFoundException, compute_grid_tree, Node
from .Canvas import Canvas

def is_node_recursive_doubling_grid_node(node: Node) -> bool:
    grid = node.get_value()
    return isinstance(grid, ReverseCoordinateDoublingGrid)

class ReverseCoordinateDoublingDisplay(Display):
    def __init__(self, display: Display):
        super().__init__()
        self.primary_display = display
        self.secondary_display = deepcopy(display)
    
    def set_grid(self, grid: Grid):
        tree = compute_grid_tree(grid)
        if is_node_recursive_doubling_grid_node(tree):
            super().set_grid(tree.get_value())
        else:
            matching_node = find_first_grid_tree_node_matching_function(tree, is_node_recursive_doubling_grid_node)
            if matching_node:
                matching_grid = matching_node.get_value()
                super().set_grid(matching_grid)
            else:
                raise GridNotFoundException('Grid is not a recursive doubling grid: ' + str(grid) + '.')

    def draw_on(self, canvas: Canvas):
        primary_grid = self.grid.get_primary_grid()
        self.primary_display.set_grid(primary_grid)
        self.primary_display.set_rectangle(self.grid.get_primary_rectangle())
        secondary_grid = self.grid.get_secondary_grid()
        self.secondary_display.set_grid(secondary_grid)
        self.secondary_display.set_rectangle(self.grid.get_secondary_rectangle())
        if self.primary_display.is_boundary_acknowledging():
            boundaries_touching = compute_boundaries_touching(
                self.grid.get_primary_rectangle(),
                self.grid.get_rectangle(),
            )
            self.primary_display.draw_on_canvas_given_boundaries_touching(canvas, boundaries_touching)
            boundaries_touching = compute_boundaries_touching(
                self.grid.get_secondary_rectangle(),
                self.grid.get_rectangle(),
            )
            self.secondary_display.draw_on_canvas_given_boundaries_touching(canvas, boundaries_touching)
        else:
            self.primary_display.draw_on(canvas)
            self.secondary_display.draw_on(canvas)
    
    @staticmethod
    def supports_grid(grid):
        return is_node_recursive_doubling_grid_node(grid)
    
    def get_name(self) -> str:
        name = 'ReverseCoordinateDoublingDisplay(' + self.primary_display.get_name() + ')'
        return name