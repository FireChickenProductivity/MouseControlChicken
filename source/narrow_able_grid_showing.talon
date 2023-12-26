tag: user.mouse_control_chicken_narrow_able_showing
mode: user.mouse_control_chicken_narrow_able_grid_mode
mode: Command
-

reset: 
    user.mouse_control_chicken_reset_narrow_able_grid()
    user.mouse_control_chicken_disable_narrow_able_grid_mode()

<user.mouse_control_chicken_coordinates> tap: 
    user.mouse_control_chicken_narrow_grid(mouse_control_chicken_coordinates)
    user.mouse_control_chicken_click_current_position_on_narrow_able_grid()
tap here: user.mouse_control_chicken_click_current_position_on_narrow_able_grid()

<user.mouse_control_chicken_coordinates> brush:
    user.mouse_control_chicken_narrow_grid(mouse_control_chicken_coordinates)
    user.mouse_control_chicken_right_click_current_position_on_narrow_able_grid()
brush here: user.mouse_control_chicken_right_click_current_position_on_narrow_able_grid()

<user.mouse_control_chicken_coordinates> hold: 
    user.mouse_control_chicken_narrow_grid(mouse_control_chicken_coordinates)
    user.mouse_control_chicken_drag_from_current_position_on_narrow_able_grid()
hold here: user.mouse_control_chicken_drag_from_current_position_on_narrow_able_grid()

<user.mouse_control_chicken_coordinates> drop:
    user.mouse_control_chicken_narrow_grid(mouse_control_chicken_coordinates)
    user.mouse_control_chicken_end_drag_at_current_position_on_narrow_able_grid()
drop here: user.mouse_control_chicken_end_drag_at_current_position_on_narrow_able_grid()

<user.mouse_control_chicken_coordinates> meet:
    user.mouse_control_chicken_narrow_grid(mouse_control_chicken_coordinates)
    user.mouse_control_chicken_move_mouse_to_position_on_narrow_able_grid()
meet here: user.mouse_control_chicken_move_mouse_to_position_on_narrow_able_grid()