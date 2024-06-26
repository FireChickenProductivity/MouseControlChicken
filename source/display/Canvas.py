import math
from talon import canvas, ui
from talon.skia import Paint, Rect
from ..grid.Grid import Rectangle
from ..SettingsMediator import settings_mediator

SMALLEST_REGULAR_BACKGROUND_RECTANGLE_HORIZONTAL_SIZE = 10
MINIMUM_BACKGROUND_RECTANGLE_VERTICAL_SIZE = 15
MINIMUM_BACKGROUND_RECTANGLE_VERTICAL_ADJUSTMENT = 10

def update_canvas_color(canvas, color: str):
    canvas.paint.color = color

def update_canvas_text_size(canvas, size: int):
    canvas.paint.textsize = size

def update_canvas_line_thickness(canvas, thickness: int):
    canvas.paint.stroke_width = thickness

class Text:
    def __init__(self, x: int, y: int, text: str):
        self.x = x
        self.y = y
        self.text = text

class Line:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class CanvasElementOptions:
    def __init__(self, size: int, color: str):
        self.size = size
        self.color = color
    
    def update(self, new_options):
        self.size = new_options.size
        self.color = new_options.color

class LineManager:
    def __init__(self, options: CanvasElementOptions):
        self.elements = []
        self.options = options
    
    def insert(self, line: Line):
        self.elements.append(line)
    
    def clear(self):
        self.elements.clear()
    
    def add_to_canvas(self, canvas):
        update_canvas_color(canvas, self.options.color)
        update_canvas_line_thickness(canvas, self.options.size)
        for line in self.elements: canvas.draw_line(line.x1, line.y1, line.x2, line.y2)

class TextManager:
    def __init__(self, options: CanvasElementOptions):
        self.elements = []
        self.options = options
    
    def insert(self, text: Text):
        self.elements.append(text)
    
    def clear(self):
        self.elements.clear()
    
    def add_to_canvas(self, canvas):
        self.add_background_rectangles_to_canvas(canvas)
        self.add_text_to_canvas(canvas)
    
    def add_background_rectangles_to_canvas(self, canvas):
        update_canvas_color(canvas, settings_mediator.get_background_color() + compute_transparency_in_hexadecimal(settings_mediator.get_background_transparency()))
        for text in self.elements: draw_background_rectangle_for_text(canvas, text, self.options.size)
    
    def add_text_to_canvas(self, canvas):
        update_canvas_color(canvas, self.options.color + compute_transparency_in_hexadecimal(settings_mediator.get_main_transparency()))
        update_canvas_text_size(canvas, self.options.size)
        for text in self.elements: draw_canvas_text(canvas, text)

def compute_transparency_in_hexadecimal(transparency) -> str:
    transparency_amount = 0xFF*(1 - transparency)
    hexadecimal = hex(round(transparency_amount))
    result = hexadecimal[2:4]
    if result == "0": result += "0"
    return result

def draw_background_rectangle_for_text(canvas, text: Text, text_size: int):
    vertical = compute_text_vertical(canvas, text)
    width = compute_background_horizontal_rectangle_size(text.text, text_size)
    height = compute_background_vertical_rectangle_size(text_size)
    vertical_adjustment = max(text_size, MINIMUM_BACKGROUND_RECTANGLE_VERTICAL_ADJUSTMENT)
    text_background_rectangle = Rect(text.x - width/2, vertical - vertical_adjustment, width, height)
    canvas.draw_rect(text_background_rectangle)

def compute_background_horizontal_rectangle_size(text: str, text_size):
    horizontal_size = math.ceil(len(text)*text_size)
    if horizontal_size < SMALLEST_REGULAR_BACKGROUND_RECTANGLE_HORIZONTAL_SIZE:
        horizontal_size += (SMALLEST_REGULAR_BACKGROUND_RECTANGLE_HORIZONTAL_SIZE - horizontal_size)/2.0
    return horizontal_size

def compute_background_vertical_rectangle_size(text_size):
    vertical_size = math.ceil(text_size*1.5)
    if vertical_size < MINIMUM_BACKGROUND_RECTANGLE_VERTICAL_SIZE:
        vertical_size += (MINIMUM_BACKGROUND_RECTANGLE_VERTICAL_SIZE - vertical_size)/2.0
    return vertical_size

def draw_canvas_text(canvas, text: Text):
    vertical = compute_text_vertical(canvas, text)
    canvas.draw_text(text.text, text.x, vertical)

def compute_text_vertical(canvas, text: Text):
    background_text_rectangle = compute_background_rectangle_for_text(canvas, text)
    return text.y + background_text_rectangle.height/2

def compute_background_rectangle_for_text(canvas, text: Text):
    return canvas.paint.measure_text(text.text)[1].copy()

def compute_line_color_with_transparency() -> str:
    color = settings_mediator.get_line_color()
    transparency = settings_mediator.get_line_transparency()
    result = color + compute_transparency_in_hexadecimal(transparency)
    return result

class Canvas:
    def __init__(self):
        self.rect = None
        self.canvas = None
        self.showing = False
        self.line_options = CanvasElementOptions(settings_mediator.get_line_width(), compute_line_color_with_transparency())
        self.text_options = CanvasElementOptions(settings_mediator.get_text_size(), settings_mediator.get_text_color())
        self.lines = LineManager(self.line_options)
        self.text = TextManager(self.text_options)

    def setup(self, rectangle: Rectangle):
        self.hide()
        screens = ui.screens()
        talon_rectangle = Rect(rectangle.left, rectangle.top, rectangle.right - rectangle.left, rectangle.bottom - rectangle.top)
        for screen in screens:
            if screen.rect == talon_rectangle:
                self.canvas = canvas.Canvas.from_screen(screen)
                return 
        self.canvas = canvas.Canvas(0, 0, rectangle.right - rectangle.left, rectangle.bottom - rectangle.top)
        self.canvas.move(rectangle.left, rectangle.top)
       
    def show(self):
        self.showing = True
        self.canvas.register("draw", self.draw)
        self.canvas.freeze()
        return 

    def draw(self, canvas):
        canvas.paint.text_align = canvas.paint.TextAlign.CENTER
        canvas.paint.style = Paint.Style.FILL
        canvas.paint.font.typeface = settings_mediator.get_font()
        self.lines.add_to_canvas(canvas)
        self.text.add_to_canvas(canvas)

    def hide(self):
        self.showing = False
        if self.canvas:
            self.canvas.close()

    def is_showing(self):
        return self.showing
    
    def refresh(self):
        if self.is_showing():
            self.hide()
            self.show()
        
    def insert_line(self, line: Line):
        self.lines.insert(line)
    
    def insert_text(self, text: Text):
        self.text.insert(text)
    
    def update_line_options(self, options: CanvasElementOptions):
        self.line_options.update(options)
    
    def update_text_options(self, options: CanvasElementOptions):
        self.text_options.update(options)
