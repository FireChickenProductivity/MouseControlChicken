tag: user.mouse_control_chicken_showing
-
meet <user.mouse_control_chicken_coordinates>: 
    user.mouse_control_chicken_move_to_position(mouse_control_chicken_coordinates)

tap <user.mouse_control_chicken_coordinates>:
    user.mouse_control_chicken_click_position(mouse_control_chicken_coordinates)

brush <user.mouse_control_chicken_coordinates>:
    user.mouse_control_chicken_right_click_position(mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> slide <user.mouse_control_chicken_coordinates>:
    user.mouse_control_chicken_drag_from_position(mouse_control_chicken_coordinates_1)
    user.mouse_control_chicken_end_drag_at_position(mouse_control_chicken_coordinates_2)

hold <user.mouse_control_chicken_coordinates>:
    user.mouse_control_chicken_drag_from_position(mouse_control_chicken_coordinates)

drop <user.mouse_control_chicken_coordinates>:
    user.mouse_control_chicken_end_drag_at_position(mouse_control_chicken_coordinates)