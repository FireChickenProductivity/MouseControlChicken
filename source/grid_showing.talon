tag: user.mouse_control_chicken_showing
mode: user.mouse_control_chicken_narrow_able_grid_mode
mode: Command
-
meet <user.mouse_control_chicken_coordinates>: 
    user.mouse_control_chicken_move_to_position(mouse_control_chicken_coordinates)

tap <user.mouse_control_chicken_coordinates>:
    user.mouse_control_chicken_click_position(mouse_control_chicken_coordinates)

pierce <user.mouse_control_chicken_coordinates>:
    user.mouse_control_chicken_double_click_position(mouse_control_chicken_coordinates)

brush <user.mouse_control_chicken_coordinates>:
    user.mouse_control_chicken_right_click_position(mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> slide <user.mouse_control_chicken_coordinates>:
    user.mouse_control_chicken_drag_from_position(mouse_control_chicken_coordinates_1)
    user.mouse_control_chicken_end_drag_at_position(mouse_control_chicken_coordinates_2)

hold <user.mouse_control_chicken_coordinates>:
    user.mouse_control_chicken_drag_from_position(mouse_control_chicken_coordinates)

drop <user.mouse_control_chicken_coordinates>:
    user.mouse_control_chicken_end_drag_at_position(mouse_control_chicken_coordinates)

chicken crisscross: user.mouse_control_chicken_toggle_frame_display_crisscross()