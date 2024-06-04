from .Display import Display, compute_boundaries_touching
from copy import deepcopy
from ..grid.ReverseCoordinateDoublingGrid import ReverseCoordinateDoublingGrid
from ..grid.Grid import Grid
from ..grid.GridCalculations import find_first_grid_tree_node_matching_function, GridNotFoundException, compute_grid_tree, Node
from .Canvas import Canvas

def is_node_recursive_doubling_grid_node(node: Node) -> bool:
    grid = node.get_value()
    return isinstance(grid, ReverseCoordinateDoublingGrid)

class ReverseCoordinateDoublingHalfDisplay():
    def __init__(self, display: Display):
        self.rectangle = None
        self.display = display
        self.main_rectangle = None
    
    def set_grid(self, grid: Grid):
        self.rectangle = grid.get_rectangle()
        self.display.set_rectangle(self.rectangle)
        self.display.set_grid(grid)
    
    def set_main_rectangle(self, main_rectangle):
        self.main_rectangle = main_rectangle

    def draw_on(self, canvas: Canvas):
        if self.display.is_boundary_acknowledging():
            boundaries_touching = compute_boundaries_touching(
                self.rectangle,
                self.main_rectangle,
            )
            self.display.draw_on_canvas_given_boundaries_touching(canvas, boundaries_touching)
        else:
            self.display.draw_on(canvas)
        
    def get_name(self) -> str:
        return self.display.get_name()

class ReverseCoordinateDoublingDisplay(Display):
    def __init__(self, display: Display):
        super().__init__()
        self.primary_display = ReverseCoordinateDoublingHalfDisplay(display)
        self.secondary_display = ReverseCoordinateDoublingHalfDisplay(deepcopy(display))
    
    def _update_grid_value(self, grid: Grid):
        self.primary_display.set_grid(grid.get_primary_grid())
        self.secondary_display.set_grid(grid.get_secondary_grid())

    def set_grid(self, grid: Grid):
        tree = compute_grid_tree(grid)
        if is_node_recursive_doubling_grid_node(tree):
            self._update_grid_value(tree.get_value())
        else:
            matching_node = find_first_grid_tree_node_matching_function(tree, is_node_recursive_doubling_grid_node)
            if matching_node:
                matching_grid = matching_node.get_value()
                self._update_grid_value(matching_grid)
            else:
                raise GridNotFoundException('Grid is not a recursive doubling grid: ' + str(grid) + '.')

    def set_rectangle(self, rectangle):
        for display in self.get_displays():
            display.set_main_rectangle(rectangle)

    def draw_on(self, canvas: Canvas):
        displays = self.get_displays()
        for display in displays:
            display.draw_on(canvas)
        
    def get_displays(self):
        return [self.primary_display, self.secondary_display]
    
    @staticmethod
    def supports_grid(grid):
        return is_node_recursive_doubling_grid_node(grid)
    
    def get_name(self) -> str:
        name = 'ReverseCoordinateDoublingDisplay(' + self.primary_display.get_name() + ')'
        return name