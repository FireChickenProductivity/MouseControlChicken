from .Grid import Rectangle
from .fire_chicken.mouse_position import MousePosition

def compute_center_position(rectangle: Rectangle) -> MousePosition:
    horizontal = compute_average(rectangle.left, rectangle.right)
    vertical = compute_average(rectangle.top, rectangle.bottom)
    center = MousePosition(int(horizontal), int(vertical))
    return center

def compute_average(*args):
    sum = 0
    for argument in args: sum += argument
    average = sum/len(args)
    return average
