from .Grid import Rectangle
from .fire_chicken.mouse_position import MousePosition
import math

def compute_center_position(rectangle: Rectangle) -> MousePosition:
    horizontal = compute_average(rectangle.left, rectangle.right)
    vertical = compute_average(rectangle.top, rectangle.bottom)
    center = MousePosition(int(horizontal), int(vertical))
    return center

class OneDimensionalLine:
    def __init__(self, start: int, ending: int):
        self.start = start
        self.ending = ending

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
        if self.number_of_divisors < number or number < 1:
            raise IndexError(f"Attempt to access nonexistent divisor number {number} with number of divisors {self.number_of_divisors}")
        position = self.start + self.division_size*number
        return position

    def compute_split(self, number: int) -> OneDimensionalLine:
        if self.number_of_divisors + 1 < number or number < 1: 
            raise IndexError(f"Attempt to access nonexistent divisor split number {number} with number of divisors {self.number_of_divisors}")
        if number == 1: 
            print("first split", number, self.compute_divisor_position(number))
            return OneDimensionalLine(self.start, self.compute_divisor_position(number))
        if number == self.number_of_divisors + 1: 
            print("final split", self.compute_divisor_position(number - 1), self.ending)
            return OneDimensionalLine(self.compute_divisor_position(number - 1), self.ending)
        print("Middle split", number, self.compute_divisor_position(number - 1), self.compute_divisor_position(number))
        return OneDimensionalLine(self.compute_divisor_position(number - 1), self.compute_divisor_position(number))

    def get_number_of_divisors(self) -> int:
        return self.number_of_divisors

class RectangleDivider:
    def __init__(self, horizontal_divider: LineDivider, vertical_divider: LineDivider):
        self.horizontal_divider = horizontal_divider
        self.vertical_divider = vertical_divider

    def compute_sub_rectangle(self, horizontal_split_number: int, vertical_split_number: int):
        horizontal_line = self.horizontal_divider.compute_split(horizontal_split_number)
        vertical_line = self.vertical_divider.compute_split(vertical_split_number)
        rectangle = Rectangle(vertical_line.start, vertical_line.ending, horizontal_line.start, horizontal_line.ending)
        return rectangle

def compute_average(*args):
    sum = 0
    for argument in args: sum += argument
    average = sum/len(args)
    return average
