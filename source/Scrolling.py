from talon import Module, actions, cron
from .SettingsMediator import settings_mediator

SCROLLING_TIME_UNIT = "100ms"

class ScrollingState:
    def __init__(self, speed: float, is_direction_down: bool = True, acceleration: int = 0):
        self.speed = speed
        self.is_direction_down = is_direction_down
        self.acceleration = acceleration
    
def scroll(scrolling_state: ScrollingState):
    value = scrolling_state.speed*settings_mediator.get_continuous_scrolling_unit()
    if not scrolling_state.is_direction_down:
        value = -value
    actions.mouse_scroll(value)
    scrolling_state.speed += scrolling_state.acceleration
    
scrolling_state: ScrollingState = None
scrolling_job = None

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_start_scrolling(speed: int, is_direction_down: bool = True, acceleration: int = 0):
        """Start scrolling the mouse in the given direction with the given speed and acceleration."""
        actions.user.mouse_control_chicken_stop_scrolling()
        global scrolling_state
        scrolling_state = ScrollingState(speed, is_direction_down, acceleration)
        global scrolling_job
        scrolling_job = cron.interval(SCROLLING_TIME_UNIT, lambda: scroll(scrolling_state))
        actions.user.mouse_control_chicken_enable_scroll_mode()
    
    def mouse_control_chicken_reverse_scrolling():
        """Reverse the direction of mouse control chicken mouse scrolling."""
        if scrolling_state:
            scrolling_state.is_direction_down = not scrolling_state.is_direction_down

    def mouse_control_chicken_stop_scrolling():
        """Stop mouse control chicken scrolling."""
        global scrolling_job
        if scrolling_job: cron.cancel(scrolling_job)
        scrolling_job = None
        global scrolling_state
        scrolling_state = None
        actions.user.mouse_control_chicken_disable_scroll_mode()

    def mouse_control_chicken_set_scrolling_speed(speed: int):
        """Set the speed of mouse control chicken scrolling."""
        if scrolling_state:
            scrolling_state.speed = speed
    
    def mouse_control_chicken_multiply_scrolling_speed(factor: float):
        """Multiply the speed of mouse control chicken scrolling by the given factor."""
        if scrolling_state:
            scrolling_state.speed = scrolling_state.speed*factor