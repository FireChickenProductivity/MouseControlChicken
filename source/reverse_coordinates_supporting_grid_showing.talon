tag: user.mouse_control_chicken_reverse_coordinates_supporting_showing
mode: user.mouse_control_chicken_narrow_able_grid_mode
mode: command
-

<user.mouse_control_chicken_coordinates> meet:
    user.mouse_control_chicken_move_to_reverse_coordinates_position(mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> down [speed <number_small>]:
    user.mouse_control_chicken_scroll_start_scroll_continuously_at_reverse_coordinates(mouse_control_chicken_coordinates, number_small or 1)

<user.mouse_control_chicken_coordinates> up [speed <number_small>]:
    user.mouse_control_chicken_scroll_start_scroll_continuously_at_reverse_coordinates(mouse_control_chicken_coordinates, number_small or 1, false)

<user.mouse_control_chicken_coordinates> {user.mouse_control_chicken_action}:
    user.mouse_control_chicken_perform_action_at_reverse_coordinates(mouse_control_chicken_action, mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> <user.modifiers> {user.mouse_control_chicken_action}:
    user.mouse_control_chicken_perform_action_at_reverse_coordinates(mouse_control_chicken_action, mouse_control_chicken_coordinates, modifiers)
