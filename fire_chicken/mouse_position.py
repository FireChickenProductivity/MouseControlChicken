import math
from talon import ctrl, actions

class MousePosition:
    COORDINATE_SEPARATOR = ' '
    def __init__(self, horizontal: int, vertical: int):
        self.horizontal = horizontal
        self.vertical = vertical
    
    def get_horizontal(self):
        return self.horizontal
    def get_vertical(self):
        return self.vertical
    
    def __add__(self, other):
        result = MousePosition(0, 0)
        result += self
        result += other
        return result
    def __iadd__(self, other):
        self.horizontal += other.horizontal
        self.vertical += other.vertical
        return self
    def __sub__(self, other):
        result = MousePosition(0, 0)
        result += self
        result -= other
        return result
    def __isub__(self, other):
        self.horizontal -= other.horizontal
        self.vertical -= other.vertical
        return self
    def __mul__(self, other):
        scaled_position = MousePosition.compute_position_scaled_by(self, other)
        return scaled_position
    def __rmul__(self, other):
        scaled_position = MousePosition.compute_position_scaled_by(self, other)
        return scaled_position

    def go(self):
        actions.mouse_move(self.horizontal, self.vertical)

    def __str__(self) -> str:
        return str(self.horizontal) + MousePosition.COORDINATE_SEPARATOR + str(self.vertical)
    
    def __repr__(self) -> str:
        return str(self)

    #assumes that the text properly represents a mouse position object
    @staticmethod
    def from_text(text: str):
        horizontal_ending = text.index(MousePosition.COORDINATE_SEPARATOR)
        horizontal = int(text[0 : horizontal_ending])
        vertical_start = horizontal_ending + 1
        vertical = int(text[vertical_start:])
        return MousePosition(horizontal, vertical)

    @staticmethod
    def current():
        horizontal, vertical = ctrl.mouse_pos()
        current_mouse_position = MousePosition(horizontal, vertical)
        return current_mouse_position
    
    def __eq__(self, other):
        return self.horizontal == other.horizontal and self.vertical == other.vertical

    def distance_from(self, other):
        return math.sqrt((self.horizontal - other.horizontal)**2 + (self.vertical - other.vertical)**2)

    def compute_magnitude(self):
        return self.distance_from(MousePosition(0, 0))

    @staticmethod
    def compute_position_scaled_by(position, number):
        if MousePosition._correct_types_for_multiplication(position, number):
            result: MousePosition = MousePosition(position.get_horizontal()*number, position.get_vertical()*number)
            return result
        return NotImplemented
    @staticmethod
    def _correct_types_for_multiplication(position, number):
        return isinstance(position, MousePosition) and (type(number) is float or type(number) is int)

