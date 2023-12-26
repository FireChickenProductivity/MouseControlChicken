from .fire_chicken.mouse_position import MousePosition
from typing import List, Generator
from .Canvas import Line, Canvas
from .MousePositionUtilities import compute_mouse_position_average

class MousePositionLine:
    def __init__(self, start: MousePosition, ending: MousePosition):
        self.start = start
        self.ending = ending

class LinearRegion:
    def __init__(self, lines: List[MousePositionLine]):
        self.lines = lines
    
    def get_lines(self) -> Generator:
        for line in self.lines: yield line

def draw_linear_region_on_canvas_with_lines_converted_to_half_lines_around_midpoint(canvas: Canvas, linear_region: LinearRegion):
    for line in linear_region.get_lines():
        half_line = compute_half_mouse_position_line_around_midpoint(line)
        draw_mouse_position_line_on_canvas(canvas, half_line)

def compute_half_mouse_position_line_around_midpoint(mouse_position_line: MousePositionLine)-> MousePositionLine:
    midpoint = compute_mouse_position_average(mouse_position_line.start, mouse_position_line.ending)
    midpoint_of_bottom_half = compute_mouse_position_average(mouse_position_line.start, midpoint)
    midpoint_of_top_half = compute_mouse_position_average(midpoint, mouse_position_line.ending)
    return MousePositionLine(midpoint_of_bottom_half, midpoint_of_top_half)

def draw_linear_region_on_canvas(canvas: Canvas, linear_region: LinearRegion):
    for line in linear_region.get_lines(): draw_mouse_position_line_on_canvas(canvas, line)

def draw_mouse_position_line_on_canvas(canvas: Canvas, mouse_position_line: MousePositionLine):
    line = create_line_from_mouse_position_line(mouse_position_line)
    canvas.insert_line(line)

def create_line_from_mouse_position_line(mouse_position_line: MousePositionLine) -> Line:
    return Line(
        mouse_position_line.start.get_horizontal(), 
        mouse_position_line.start.get_vertical(), 
        mouse_position_line.ending.get_horizontal(), 
        mouse_position_line.ending.get_vertical()
    )