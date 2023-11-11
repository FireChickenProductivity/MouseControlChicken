from talon import canvas
from talon.skia import Paint
from .Grid import Rectangle

def update_canvas_color(canvas, color: str):
    canvas.paint.color = "FF0000"

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
        update_canvas_color(canvas, self.options.color)
        update_canvas_text_size(canvas, self.options.size)
        for text in self.elements: canvas.draw_text(text.text, text.x, text.y)

class Canvas:
    def __init__(self):
        self.rect = None
        self.canvas = None
        self.showing = False
        self.lines = LineManager(CanvasElementOptions(2, "FF0000"))
        self.text = TextManager(CanvasElementOptions(30, "FF0000"))
        self.text.insert(Text(50, 50, 'St'))
        self.lines.insert(Line(10, 10, 30, 30))

    def setup(self, rectangle: Rectangle):
        self.hide()
        self.canvas = canvas.Canvas(0, 0, rectangle.right - rectangle.left, rectangle.bottom - rectangle.top)
        self.canvas.move(rectangle.left, rectangle.top)
       
    def show(self, rectangle: Rectangle):
        self.setup(rectangle)
        self.showing = True
        self.canvas.register("draw", self.draw)
        self.canvas.freeze()
        return 

    def draw(self, canvas):
        canvas.paint.text_align = canvas.paint.TextAlign.CENTER
        canvas.paint.style = Paint.Style.FILL
        self.lines.add_to_canvas(canvas)
        self.text.add_to_canvas(canvas)
        print(canvas.rect)

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
experiment = Canvas().show(Rectangle(0, 1000, 0, 1000))
