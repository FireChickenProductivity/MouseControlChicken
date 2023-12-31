from ..fire_chicken.mouse_position import MousePosition
from ..SettingsMediator import settings_mediator
from .Canvas import compute_background_horizontal_rectangle_size, compute_background_vertical_rectangle_size
from typing import List

class Skipper:
    """A skipper object determines if a display should skip showing something"""
    def should_include_position_with_text(self, position: MousePosition, text: str) -> bool:
        pass

    def handle_position_included(self, position: MousePosition):
        pass

    def handle_position_excluded(self, position: MousePosition):
        pass

class SkipperComposite(Skipper):
    """A skipper union object contains multiple skippers and determines if a display should skip showing something of any of these skippers decides it should not show the position"""
    def __init__(self, skippers: List[Skipper]):
        self.skippers = skippers

    def should_include_position_with_text(self, position: MousePosition, text: str) -> bool:
        for skipper in self.skippers:
            if not skipper.should_include_position_with_text(position, text):
                return False
        return True

    def handle_position_included(self, position: MousePosition):
        for skipper in self.skippers:
            skipper.handle_position_included(position)

    def handle_position_excluded(self, position: MousePosition):
        for skipper in self.skippers:
            skipper.handle_position_excluded(position)

class HorizontalSkipper(Skipper):
    def __init__(self):
        self.last_horizontal = None

    def should_include_position_with_text(self, position: MousePosition, text: str) -> bool:
        return self.last_horizontal is None or \
            abs(position.get_horizontal() - self.last_horizontal) >= compute_background_horizontal_rectangle_size(text, settings_mediator.get_text_size())

    def handle_position_included(self, position: MousePosition):
        self.last_horizontal = position.get_horizontal()

class VerticalSkipper(Skipper):
    def __init__(self):
        self.last_vertical = None

    def should_include_position_with_text(self, position: MousePosition, text: str) -> bool:
        return self.last_vertical is None or \
            abs(position.get_vertical() - self.last_vertical) >= compute_background_vertical_rectangle_size(settings_mediator.get_text_size())

    def handle_position_included(self, position: MousePosition):
        self.last_vertical = position.get_vertical()

def create_rectangular_skipper():
    composite = SkipperComposite([HorizontalSkipper(), VerticalSkipper()])
    return composite
    
class CheckerSkipper(Skipper):
    """A checker skipper skips every nth position"""
    def __init__(self, n: int):
        self.n = n
        self.count = 0

    def should_include_position_with_text(self, position: MousePosition, text: str) -> bool:
        return self.count == self.n - 1

    def handle_position_included(self, position: MousePosition):
        self.count = 0

    def handle_position_excluded(self, position: MousePosition):
        self.count += 1
    
def create_rectangular_checker_skipper(n: int):
    return SkipperComposite([create_rectangular_skipper(), CheckerSkipper(n)])

class SkipperRunner:
    def __init__(self, Skipper: Skipper):
        self.skipper = Skipper
        self.generator = None
        self.position_creator = None
        self.on_inclusion = None
    
    def set_generator(self, generator):
        self.generator = generator
    
    def set_position_creator(self, position_creator):
        self.position_creator = position_creator
    
    def set_on_inclusion(self, on_inclusion):
        self.on_inclusion = on_inclusion
    
    def run(self):
        for item in self.generator:
            position = self.position_creator(item)
            if self.skipper.should_include_position_with_text(position, item):
                self.skipper.handle_position_included(position)
                self.on_inclusion(item, position)
            else:
                self.skipper.handle_position_excluded(position)
