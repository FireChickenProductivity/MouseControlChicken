from ..fire_chicken.mouse_position import MousePosition
from ..SettingsMediator import settings_mediator
from .Canvas import compute_background_horizontal_rectangle_size, compute_background_vertical_rectangle_size
from typing import List

class Skipper:
    """A skipper object determines if a display should skip showing something"""
    def should_include_position_with_text(self, position: MousePosition, text: str) -> bool:
        pass

    def update_last_horizontal(self, horizontal: int):
        pass

    def update_last_vertical(self, vertical: int):
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

    def update_last_horizontal(self, horizontal: int):
        for skipper in self.skippers:
            skipper.update_last_horizontal(horizontal)

    def update_last_vertical(self, vertical: int):
        for skipper in self.skippers:
            skipper.update_last_vertical(vertical)

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

    def update_last_horizontal(self, horizontal: int):
        self.last_horizontal = horizontal

class VerticalSkipper(Skipper):
    def __init__(self):
        self.last_vertical = None

    def should_include_position_with_text(self, position: MousePosition, text: str) -> bool:
        return self.last_vertical is None or \
            abs(position.get_vertical() - self.last_vertical) >= compute_background_vertical_rectangle_size(settings_mediator.get_text_size())

    def update_last_vertical(self, vertical: int):
        self.last_vertical = vertical

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
