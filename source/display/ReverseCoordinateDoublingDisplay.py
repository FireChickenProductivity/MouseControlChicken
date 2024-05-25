from .Display import Display, BoundariesTouching, compute_boundaries_touching
from copy import deepcopy
from ..grid.ReverseCoordinateDoublingGrid import ReverseCoordinateDoublingGrid
from .Canvas import Canvas

class ReverseCoordinateDoublingDisplay(Display):
    def __init__(self, display: Display):
        super().__init__()
        self.primary_display = display
        self.secondary_display = deepcopy(display)
    
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
        return isinstance(grid, ReverseCoordinateDoublingGrid)
    
    def get_name(self) -> str:
        name = 'ReverseCoordinateDoublingDisplay(' + self.primary_display.get_name() + ')'
        return name