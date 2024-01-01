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

class SingleNestedSkipperRunner:
    def __init__(self, outer_skipper: Skipper, inner_skipper: Skipper):
        self.outer_skipper = outer_skipper
        self.inner_skipper = inner_skipper
        self.outer_generator = None
        self.inner_generator_creation_function = None
        self.outer_value_creator = None
        self.inner_position_creator = None
        self.outer_position_creator = None
        self.on_inclusion = None
    
    def set_outer_generator(self, outer_generator):
        self.outer_generator = outer_generator
    
    def set_inner_generator_creation_function(self, inner_generator_creation_function):
        """The inner generator creation function returns a generator"""
        self.inner_generator_creation_function = inner_generator_creation_function
    
    def set_outer_value_creator(self, outer_value_creator):
        """The outer value creator receives the outer item as an argument and returns a value"""
        self.outer_value_creator = outer_value_creator
    
    def set_inner_position_creator(self, inner_position_creator):
        """The inner position creator receives the inner item and the outer value as arguments and returns a MousePosition"""
        self.inner_position_creator = inner_position_creator
    
    def set_outer_position_creator(self, outer_position_creator):
        """The outer position creator receives the outer item and the outer value as arguments and returns a MousePosition"""
        self.outer_position_creator = outer_position_creator
      
    def set_on_inclusion(self, on_inclusion):
        """The on inclusion function receives the outer item, the inner item, and the inner position as arguments"""
        self.on_inclusion = on_inclusion
    
    def run(self):
        for outer_item in self.outer_generator:
            outer_value = self.outer_value_creator(outer_item)
            outer_position = self.outer_position_creator(outer_item, outer_value)
            if self.outer_skipper.should_include_position_with_text(outer_position, outer_item):
                self.outer_skipper.handle_position_included(outer_position)
                self.handle_inner_loop(outer_item, outer_value)
            else:
                self.outer_skipper.handle_position_excluded(outer_position)
            
    def handle_inner_loop(self, outer_item, outer_value):
        for inner_item in self.inner_generator_creation_function():
            inner_position = self.inner_position_creator(inner_item, outer_value)
            if self.inner_skipper.should_include_position_with_text(inner_position, inner_item):
                self.inner_skipper.handle_position_included(inner_position)
                self.on_inclusion(outer_item, inner_item, inner_position)
            else:
                self.inner_skipper.handle_position_excluded(inner_position)
    