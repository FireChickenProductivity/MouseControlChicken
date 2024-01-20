from talon import Module, actions
from .SettingsMediator import settings_mediator
from .fire_chicken.mouse_position import MousePosition

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_click_position(coordinates: str):
        '''Clicks the specified position on the current mouse control chicken grid'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        actions.mouse_click()

    def mouse_control_chicken_double_click_position(coordinates: str):
        '''Double clicks the specified position on the current mouse control chicken grid'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        double_click()
    
    def mouse_control_chicken_right_click_position(coordinates: str):
        '''Clicks the specified position on the current mouse control chicken grid'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        actions.mouse_click(1)
    
    def mouse_control_chicken_drag_from_position(coordinates: str):
        '''Moves the mouse to the specified position on the current mouse control chicken position and starts dragging'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        drag_from_position()
    
    def mouse_control_chicken_end_drag_at_position(coordinates: str):
        '''Moves the mouse to the specified position on the current mouse control chicken position and stops dragging'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        end_drag_at_position()

    def mouse_control_chicken_scroll_up_at_position(coordinates: str):
        '''Moves the mouse to the specified position on the current mouse control chicken position and scrolls up'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        scroll_up()
    
    def mouse_control_chicken_scroll_down_at_position(coordinates: str):
        '''Moves the mouse to the specified position on the current mouse control chicken position and scrolls down'''
        actions.user.mouse_control_chicken_move_to_position(coordinates)
        scroll_down()
    
    def mouse_control_chicken_click_current_position_on_narrow_able_grid():
        '''Clicks the current position on the current mouse control chicken grid'''
        if manager_has_narrow_able_grid():
            position = get_current_position_on_narrow_able_grid()
            position.go()
            actions.mouse_click()
            actions.user.mouse_control_chicken_reset_narrow_able_grid()
            actions.user.mouse_control_chicken_disable_narrow_able_grid_mode()
        
    def mouse_control_chicken_double_click_current_position_on_narrow_able_grid():
        '''Double clicks the current position on the current mouse control chicken grid'''
        if manager_has_narrow_able_grid():
            position = get_current_position_on_narrow_able_grid()
            position.go()
            double_click()
            actions.user.mouse_control_chicken_reset_narrow_able_grid()
            actions.user.mouse_control_chicken_disable_narrow_able_grid_mode()
        
    def mouse_control_chicken_right_click_current_position_on_narrow_able_grid():
        '''Right clicks the current position on the current mouse control chicken grid'''
        if manager_has_narrow_able_grid():
            position = get_current_position_on_narrow_able_grid()
            position.go()
            actions.mouse_click(1)
            actions.user.mouse_control_chicken_reset_narrow_able_grid()
            actions.user.mouse_control_chicken_disable_narrow_able_grid_mode()
        
    def mouse_control_chicken_drag_from_current_position_on_narrow_able_grid():
        '''Starts dragging from the current position on the current mouse control chicken grid'''
        if manager_has_narrow_able_grid():
            position = get_current_position_on_narrow_able_grid()
            position.go()
            drag_from_position()
            actions.user.mouse_control_chicken_reset_narrow_able_grid()
            actions.user.mouse_control_chicken_disable_narrow_able_grid_mode()
    
    def mouse_control_chicken_end_drag_at_current_position_on_narrow_able_grid():
        '''Ends dragging at the current position on the current mouse control chicken narrow able grid'''
        if manager_has_narrow_able_grid():
            position = get_current_position_on_narrow_able_grid()
            position.go()
            end_drag_at_position()
            actions.user.mouse_control_chicken_reset_narrow_able_grid()
            actions.user.mouse_control_chicken_disable_narrow_able_grid_mode()

    def mouse_control_chicken_move_mouse_to_position_on_narrow_able_grid():
        '''Moves the mouse to the current position on the current mouse control chicken narrow able grid'''
        if manager_has_narrow_able_grid():
            position = get_current_position_on_narrow_able_grid()
            position.go()
            actions.user.mouse_control_chicken_reset_narrow_able_grid()
            actions.user.mouse_control_chicken_disable_narrow_able_grid_mode()
        
    def mouse_control_chicken_scroll_up_at_current_position_on_narrow_able_grid():
        '''Scrolls up at the current position on the current mouse control chicken narrow able grid'''
        if manager_has_narrow_able_grid():
            position = get_current_position_on_narrow_able_grid()
            position.go()
            scroll_up()
            actions.user.mouse_control_chicken_reset_narrow_able_grid()
            actions.user.mouse_control_chicken_disable_narrow_able_grid_mode()
        
    def mouse_control_chicken_scroll_down_at_current_position_on_narrow_able_grid():
        '''Scrolls down at the current position on the current mouse control chicken narrow able grid'''
        if manager_has_narrow_able_grid():
            position = get_current_position_on_narrow_able_grid()
            position.go()
            scroll_down()
            actions.user.mouse_control_chicken_reset_narrow_able_grid()
            actions.user.mouse_control_chicken_disable_narrow_able_grid_mode()

def get_position_on_grid(coordinates: str) -> MousePosition:
    position = actions.user.mouse_control_chicken_get_position_on_grid(coordinates)
    return position

def get_current_position_on_narrow_able_grid() -> MousePosition:
    position = actions.user.mouse_control_chicken_get_current_position_on_narrow_able_grid()
    return position

def manager_has_narrow_able_grid() -> bool:
    return actions.user.mouse_control_chicken_is_using_narrow_able_grid()

def drag_from_position():
    actions.sleep(0.5)
    actions.user.mouse_drag(0)

def end_drag_at_position():
    actions.sleep(0.5)
    actions.user.mouse_drag_end()

def double_click():
    actions.mouse_click()
    actions.mouse_click()

def scroll_up():
    actions.mouse_scroll(-settings_mediator.get_scrolling_amount())

def scroll_down():
    actions.mouse_scroll(settings_mediator.get_scrolling_amount())
