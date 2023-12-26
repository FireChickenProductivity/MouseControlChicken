from .Display import Display
from .Grid import Grid, Rectangle, RecursiveDivisionGrid
from .Canvas import Canvas, Text, Line
from .UniversalDisplays import UniversalPositionDisplay
from .Regions import draw_linear_region_on_canvas

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
        for region in self.grid.get_regions():
            draw_linear_region_on_canvas(self.canvas, region)
        
    def supports_grid(grid: Grid) -> bool:
        return isinstance(grid, RecursiveDivisionGrid)