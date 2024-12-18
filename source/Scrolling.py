from talon import Module, actions, cron
from .SettingsMediator import settings_mediator

SCROLLING_TIME_UNIT = 100

class ScrollingState:
    def __init__(self, speed: float, is_direction_down: bool = True, acceleration: int = 0):
        self.speed = speed
        self.is_direction_down = is_direction_down
        self.acceleration = acceleration

def adjusts_scrolling_value_based_on_direction(value, is_direction_down):
    return value if is_direction_down else -value

def scroll_amount(value, is_direction_down):
    value *= settings_mediator.get_continuous_scrolling_unit()
    value = adjusts_scrolling_value_based_on_direction(value, is_direction_down)
    actions.mouse_scroll(value)

def scroll(scrolling_state: ScrollingState):
    scroll_amount(scrolling_state.speed, scrolling_state.is_direction_down)
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
        scrolling_job = cron.interval(f"{SCROLLING_TIME_UNIT}ms", lambda: scroll(scrolling_state))
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
        
    def mouse_control_chicken_scroll_amount_during_continuous_scrolling(amount: int, is_direction_same: bool = True):
        """Immediately scrolls the specified amount in the specified direction during continuous scrolling."""
        direction = scrolling_state.is_direction_down
        second_adjusted_amount = amount*(1000/SCROLLING_TIME_UNIT)
        if not is_direction_same:
            direction = not direction
        scroll_amount(second_adjusted_amount, direction)