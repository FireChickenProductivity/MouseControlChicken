from .Display import Display
from ..Grid import Grid, Rectangle, RecursiveDivisionGrid
from .UniversalDisplays import UniversalPositionDisplay
from ..Regions import draw_linear_region_on_canvas, draw_linear_region_on_canvas_with_lines_converted_to_half_lines_around_midpoint

class NarrowDisplay(Display):
    def __init__(self):
        super().__init__()
        self.grid: RecursiveDivisionGrid = None
        self.position_display: UniversalPositionDisplay = UniversalPositionDisplay()
    
    def set_grid(self, grid: RecursiveDivisionGrid):
        super().set_grid(grid)
        self.position_display.set_grid(grid)
    
    def show(self):
        super().show()
        self.position_display.show()
    
    def hide(self):
        super().hide()
        self.position_display.hide()
    
    def refresh(self):
        super().refresh()
        self.position_display.refresh()
    
    def set_rectangle(self, rectangle: Rectangle):
        self._perform_pre_drawing_setup_given_new_rectangle(rectangle)
        self.position_display.set_rectangle(rectangle)
        self._draw_region_rectangles()

    def _draw_region_rectangles(self):
        for region in self.grid.get_regions():
            draw_linear_region_on_canvas(self.canvas, region)
        
    def supports_grid(grid: Grid) -> bool:
        return isinstance(grid, RecursiveDivisionGrid)

class DoubleNarrowDisplay(NarrowDisplay):
    def set_rectangle(self, rectangle: Rectangle):
        super().set_rectangle(rectangle)
        for primary_coordinate in self.grid.get_coordinate_system().get_primary_coordinates():
            regions = self.grid.get_regions_for_sub_grid_at_coordinates(primary_coordinate)
            for region in regions:
                draw_linear_region_on_canvas_with_lines_converted_to_half_lines_around_midpoint(self.canvas, region)
        