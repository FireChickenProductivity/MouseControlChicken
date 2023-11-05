from talon import canvas
from talon.skia import Paint
from .Grid import Rectangle

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

class ElementManager:
    def __init__(self):
        self.elements = []
    
    def insert(self, element):
        self.elements.append(element)
    
    def clear(self):
        self.elements.clear()
    
    def __iter__(self):
        for element in self.elements:
            yield element

class Canvas:
    def __init__(self):
        self.rect = None
        self.canvas = None
        self.showing = False
        self.lines = ElementManager()
        self.text = ElementManager()
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
        paint = canvas.paint
        paint.textsize = 40
        canvas.paint.text_align = canvas.paint.TextAlign.CENTER
        paint.color = "FF0000"
        paint.style = Paint.Style.FILL
        for line in self.lines: canvas.draw_line(line.x1, line.y1, line.x2, line.y2)
        for text in self.text: canvas.draw_text(text.text, text.x, text.y)
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