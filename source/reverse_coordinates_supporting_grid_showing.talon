tag: user.mouse_control_chicken_reverse_coordinates_supporting_showing
mode: user.mouse_control_chicken_narrow_able_grid_mode
mode: command
-

<user.mouse_control_chicken_coordinates> tap: 
    user.mouse_control_chicken_click_reverse_coordinates_position(mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> pierce:
    user.mouse_control_chicken_double_click_reverse_coordinates_position(mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> brush:
    user.mouse_control_chicken_right_click_reverse_coordinates_position(mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> hold: 
    user.mouse_control_chicken_drag_from_reverse_coordinates_position(mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> drop:
    user.mouse_control_chicken_end_drag_at_reverse_coordinates_position(mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> meet:
    user.mouse_control_chicken_move_to_reverse_coordinates_position(mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> twist:
    user.mouse_control_chicken_scroll_up_at_reverse_coordinates_position(mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> roll:
    user.mouse_control_chicken_scroll_down_at_reverse_coordinates_position(mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> down [speed <number_small>]:
    user.mouse_control_chicken_scroll_start_scroll_continuously_at_reverse_coordinates(mouse_control_chicken_coordinates, number_small or 1)

<user.mouse_control_chicken_coordinates> up [speed <number_small>]:
    user.mouse_control_chicken_scroll_start_scroll_continuously_at_reverse_coordinates(mouse_control_chicken_coordinates, number_small or 1, false)