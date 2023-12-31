from ..fire_chicken.mouse_position import MousePosition
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