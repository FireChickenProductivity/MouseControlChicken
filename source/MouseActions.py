from talon import Module, actions
from .SettingsMediator import settings_mediator
from .fire_chicken.mouse_position import MousePosition
from .GridSystemManager import REVERSE_COORDINATES_PREFIX, PREFIX_POSTFIX

LAST_DRAG_POSITION: MousePosition = None

def compute_reverse_coordinates_string(coordinates: str) -> str:
    return REVERSE_COORDINATES_PREFIX + PREFIX_POSTFIX + coordinates

def get_position_on_grid(coordinates: str) -> MousePosition:
    position = actions.user.mouse_control_chicken_get_position_on_grid(coordinates)
    return position

def get_current_position_on_narrow_able_grid() -> MousePosition:
    position = actions.user.mouse_control_chicken_get_current_position_on_narrow_able_grid()
    return position

def manager_has_narrow_able_grid() -> bool:
    return actions.user.mouse_control_chicken_is_using_narrow_able_grid()

def drag_from_position():
    actions.sleep(settings_mediator.get_dragging_delay())
    actions.user.mouse_drag(0)

def end_drag_at_position():
    global LAST_DRAG_POSITION
    actions.sleep(settings_mediator.get_dragging_delay())
    LAST_DRAG_POSITION = MousePosition.current()
    actions.user.mouse_drag_end()

def drag_back_to_last_drag_position():
    global LAST_DRAG_POSITION
    if LAST_DRAG_POSITION is not None:
        drag_from_position()
        actions.sleep(settings_mediator.get_dragging_delay())
        LAST_DRAG_POSITION.go()
        end_drag_at_position()

def double_click():
    actions.mouse_click()
    actions.mouse_click()

def scroll_up():
    actions.mouse_scroll(-settings_mediator.get_scrolling_amount())

def scroll_down():
    actions.mouse_scroll(settings_mediator.get_scrolling_amount())

ACTION_MAP = {
    "click": actions.mouse_click,
    "double_click": double_click,
    "right_click": lambda: actions.mouse_click(1),
    "drag": drag_from_position,
    "end_drag": end_drag_at_position,
    "drag_back": drag_back_to_last_drag_position,
    "scroll_up": scroll_up,
    "scroll_down": scroll_down,
}

def performed_action_from_map(action_name: str):
    action = ACTION_MAP[action_name]
    action()

def perform_action_from_map_at_coordinates(action_name: str, coordinates: str):
    position = get_position_on_grid(coordinates)
    position.go()
    performed_action_from_map(action_name)
    actions.user.mouse_control_chicken_handle_action_using_coordinates(coordinates)

def perform_action_on_narrow_able_grid_center(action):
    if manager_has_narrow_able_grid():
        position = get_current_position_on_narrow_able_grid()
        position.go()
        action()
        actions.user.mouse_control_chicken_reset_narrow_able_grid()
        actions.user.mouse_control_chicken_disable_narrow_able_grid_mode()

def perform_action_from_map_at_reverse_coordinates(action_name: str, coordinates: str):
    reverse_coordinates = compute_reverse_coordinates_string(coordinates)
    actions.user.mouse_control_chicken_handle_reverse_coordinate_action_setup_using_coordinates(coordinates)
    perform_action_from_map_at_coordinates(action_name, reverse_coordinates)
    actions.user.mouse_control_chicken_handle_reverse_coordinate_action_cleanup()

def perform_action_on_reverse_coordinates(coordinates, action):
    actions.user.mouse_control_chicken_handle_reverse_coordinate_action_setup_using_coordinates(coordinates)
    action(compute_reverse_coordinates_string(coordinates))
    actions.user.mouse_control_chicken_handle_reverse_coordinate_action_cleanup()

module = Module()
module.list("mouse_control_chicken_action", desc="List of actions that can be performed on mouse control chicken grids")
@module.action_class
class Actions:
    def mouse_control_chicken_perform_action_at_coordinates(action_name: str, coordinates: str):
        '''Performs the specified action at the specified coordinates on the current mouse control chicken grid'''
        perform_action_from_map_at_coordinates(action_name, coordinates)

    def mouse_control_chicken_perform_action_at_reverse_coordinates(action_name: str, coordinates: str):
        '''Performs the specified action at the specified coordinates on the current mouse control chicken grid using reverse coordinates'''
        perform_action_from_map_at_reverse_coordinates(action_name, coordinates)
        
    def mouse_control_chicken_move_only_to_position(coordinates: str):
        '''Moves the mouse to the specified position on the current mouse control chicken grid and handle that as a complete action'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        actions.user.mouse_control_chicken_handle_action_using_coordinates(coordinates)

    def mouse_control_chicken_click_position(coordinates: str):
        '''Clicks the specified position on the current mouse control chicken grid'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        actions.mouse_click()
        actions.user.mouse_control_chicken_handle_action_using_coordinates(coordinates)

    def mouse_control_chicken_drag_from_position(coordinates: str):
        '''Moves the mouse to the specified position on the current mouse control chicken position and starts dragging'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        drag_from_position()
        actions.user.mouse_control_chicken_handle_action_using_coordinates(coordinates)
    
    def mouse_control_chicken_end_drag_at_position(coordinates: str):
        '''Moves the mouse to the specified position on the current mouse control chicken position and stops dragging'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        end_drag_at_position()
        actions.user.mouse_control_chicken_handle_action_using_coordinates(coordinates)

    def mouse_control_chicken_scroll_continuously_at_position(coordinates: str, speed: int, is_direction_down: bool = True):
        '''Moves the mouse to the specified position on the current mouse control chicken position and starts continuous scrolling'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        actions.user.mouse_control_chicken_start_scrolling(speed, is_direction_down)
        actions.user.mouse_control_chicken_handle_action_using_coordinates(coordinates)

    def mouse_control_chicken_move_mouse_to_position_on_narrow_able_grid():
        '''Moves the mouse to the current position on the current mouse control chicken narrow able grid'''
        if manager_has_narrow_able_grid():
            position = get_current_position_on_narrow_able_grid()
            position.go()
            actions.user.mouse_control_chicken_reset_narrow_able_grid()
            actions.user.mouse_control_chicken_disable_narrow_able_grid_mode()
        
    def mouse_control_chicken_perform_action_at_current_position_on_narrow_able_grid(action_name: str):
        '''Performs the specified action at the current position on the current mouse control chicken narrow able grid'''
        perform_action_on_narrow_able_grid_center(lambda: performed_action_from_map(action_name))

    def mouse_control_chicken_start_scrolling_at_current_position_on_narrow_able_grid(speed: int, is_direction_down: bool = True):
        ''''Starts scrolling at the current position on the current mouse control chicken narrow able grid'''
        perform_action_on_narrow_able_grid_center(lambda: actions.user.mouse_control_chicken_start_scrolling(speed, is_direction_down))

@module.action_class
class ReverseCoordinateActions:
    def mouse_control_chicken_move_to_reverse_coordinates_position(coordinates: str):
        '''Moves the mouse to the specified position on the current mouse control chicken grid using reverse coordinates'''
        perform_action_on_reverse_coordinates(coordinates, actions.user.mouse_control_chicken_move_to_position)
    
    def mouse_control_chicken_scroll_start_scroll_continuously_at_reverse_coordinates(coordinates: str, speed: int, is_direction_down: bool = True):
        '''Starts scrolling at the specified position on the current mouse control chicken grid using reverse coordinates'''
        perform_action_on_reverse_coordinates(coordinates, lambda coordinates: actions.user.mouse_control_chicken_scroll_continuously_at_position(coordinates, speed, is_direction_down))

