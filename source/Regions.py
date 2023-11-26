from .fire_chicken.mouse_position import MousePosition
from typing import List, Generator

class MousePositionLine:
    def __init__(self, start: MousePosition, ending: MousePosition):
        self.start = start
        self.ending = ending

class LinearRegion:
    def __init__(self, lines: List[MousePositionLine]):
        self.lines = lines
    
    def get_lines(self) -> Generator:
        for line in self.lines: yield line

