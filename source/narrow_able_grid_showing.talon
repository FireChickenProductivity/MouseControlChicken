tag: user.mouse_control_chicken_narrow_able_showing
-

reset: user.mouse_control_chicken_reset_narrow_able_grid()
seek <user.mouse_control_chicken_coordinates>: user.mouse_control_chicken_narrow_grid(mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> tap: 
    user.mouse_control_chicken_narrow_grid(mouse_control_chicken_coordinates)
    user.mouse_control_chicken_click_current_position_on_narrow_able_grid()
tap this: user.mouse_control_chicken_click_current_position_on_narrow_able_grid()

<user.mouse_control_chicken_coordinates> brush:
    user.mouse_control_chicken_narrow_grid(mouse_control_chicken_coordinates)
    user.mouse_control_chicken_right_click_current_position_on_narrow_able_grid()
brush this: user.mouse_control_chicken_right_click_current_position_on_narrow_able_grid()

<user.mouse_control_chicken_coordinates> hold: 
    user.mouse_control_chicken_narrow_grid(mouse_control_chicken_coordinates)
    user.mouse_control_chicken_drag_from_current_position_on_narrow_able_grid()
hold this: user.mouse_control_chicken_drag_from_current_position_on_narrow_able_grid()