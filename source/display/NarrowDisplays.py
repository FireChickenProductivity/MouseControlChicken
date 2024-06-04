from .Display import Display
from .Canvas import Canvas
from ..grid.Grid import Grid, Rectangle, RecursiveDivisionGrid
from ..grid.GridCalculations import compute_primary_grid
from .UniversalDisplays import UniversalPositionDisplay
from ..Regions import draw_linear_region_on_canvas, draw_linear_region_on_canvas_with_lines_converted_to_half_lines_around_midpoint

class NarrowDisplay(Display):
    def __init__(self):
        super().__init__()
        self.grid: RecursiveDivisionGrid = None
        self.position_display: UniversalPositionDisplay = UniversalPositionDisplay()
    
    def set_grid(self, grid: RecursiveDivisionGrid):
        primary_grid = compute_primary_grid(grid)
        super().set_grid(primary_grid)
        self.position_display.set_grid(primary_grid)
    
    def set_rectangle(self, rectangle: Rectangle):
        super().set_rectangle(rectangle)
        self.position_display.set_rectangle(rectangle)
    
    def draw_on(self, canvas):
        self.position_display.draw_on(canvas)
        self._draw_region_rectangles(canvas)

    def _draw_region_rectangles(self, canvas: Canvas):
        for region in self.grid.get_regions():
            draw_linear_region_on_canvas(canvas, region)
        
    def supports_grid(grid: Grid) -> bool:
        primary_grid = compute_primary_grid(grid)
        return isinstance(primary_grid, RecursiveDivisionGrid)

class DoubleNarrowDisplay(NarrowDisplay):
    def draw_on(self, canvas):
        super().draw_on(canvas)
        for primary_coordinate in self.grid.get_coordinate_system().get_primary_coordinates():
            regions = self.grid.get_regions_for_sub_grid_at_coordinates(primary_coordinate)
            for region in regions:
                draw_linear_region_on_canvas_with_lines_converted_to_half_lines_around_midpoint(canvas, region)
        