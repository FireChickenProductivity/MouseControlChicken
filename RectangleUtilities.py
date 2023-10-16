from .Grid import Rectangle
from .fire_chicken.mouse_position import MousePosition
import math

def compute_center_position(rectangle: Rectangle) -> MousePosition:
    horizontal = compute_average(rectangle.left, rectangle.right)
    vertical = compute_average(rectangle.top, rectangle.bottom)
    center = MousePosition(int(horizontal), int(vertical))
    return center

class LineDivider:
    def __init__(self, start: int, ending: int, number_of_divisors: int):
        self.start = start
        self.ending = ending
        self.number_of_divisors = number_of_divisors
        self._compute_division_size()
    
    def _compute_division_size(self) -> None:
        self.division_size = math.ceil(self.ending - self.start)/(self.number_of_divisors + 1)
        if self.start + int(self.division_size*self.number_of_divisors) > self.ending: 
            self.number_of_divisors = math.floor((self.ending - self.start)/(self.division_size))

    def compute_divisor_position(self, number: int) -> int:
        position = self.start + self.division_size*number
        return position

    def get_number_of_divisors(self) -> int:
        return self.number_of_divisors


def compute_average(*args):
    sum = 0
    for argument in args: sum += argument
    average = sum/len(args)
    return average
