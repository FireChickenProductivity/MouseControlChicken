tag: user.mouse_control_chicken_showing
mode: user.mouse_control_chicken_narrow_able_grid_mode
mode: command
-
meet <user.mouse_control_chicken_coordinates>: 
    user.mouse_control_chicken_move_only_to_position(mouse_control_chicken_coordinates)

{user.mouse_control_chicken_action} <user.mouse_control_chicken_coordinates>:
    user.mouse_control_chicken_perform_action_at_coordinates(mouse_control_chicken_action, mouse_control_chicken_coordinates)

<user.mouse_control_chicken_coordinates> slide <user.mouse_control_chicken_coordinates>:
    user.mouse_control_chicken_drag_from_position(mouse_control_chicken_coordinates_1)
    user.mouse_control_chicken_end_drag_at_position(mouse_control_chicken_coordinates_2)

down <user.mouse_control_chicken_coordinates> [speed <number_small>]:
    user.mouse_control_chicken_scroll_continuously_at_position(mouse_control_chicken_coordinates, number_small or 1)

up <user.mouse_control_chicken_coordinates> [speed <number_small>]:
    user.mouse_control_chicken_scroll_continuously_at_position(mouse_control_chicken_coordinates, number_small or 1, false)

chicken crisscross: user.mouse_control_chicken_toggle_frame_display_crisscross()
chicken checker [frequency] <number_small>: user.mouse_control_chicken_set_checker_frequency(number_small)
chicken frame checker [frequency] <number_small>: user.mouse_control_chicken_set_frame_checker_frequency(number_small)
chicken zigzag [threshold] <number_small>: user.mouse_control_chicken_set_zigzag_threshold(number_small)
chicken flicker: user.mouse_control_chicken_toggle_flicker_display()
chicken flicker transparency: user.mouse_control_chicken_toggle_transparency_flicker()
chicken [text] size <number_small>: user.mouse_control_chicken_set_text_size(number_small)
chicken [main] (transparency|transparent) <user.mouse_control_chicken_percentage>:
    user.mouse_control_chicken_set_main_transparency(mouse_control_chicken_percentage)
chicken (back|background) (transparency|transparent) <user.mouse_control_chicken_percentage>:
    user.mouse_control_chicken_set_background_transparency(mouse_control_chicken_percentage)
chicken line width <number_small>: user.mouse_control_chicken_set_line_width(number_small)
chicken horizontal (procs|proximity) <number>: user.mouse_control_chicken_set_horizontal_proximity_frame_distance(number)
chicken vertical (procs|proximity) <number>: user.mouse_control_chicken_set_vertical_proximity_frame_distance(number)
chicken text color <user.mouse_control_chicken_color_name>: user.mouse_control_chicken_set_text_color(mouse_control_chicken_color_name)
chicken (back|background) color <user.mouse_control_chicken_color_name>: user.mouse_control_chicken_set_background_color(mouse_control_chicken_color_name)
chicken line color <user.mouse_control_chicken_color_name>: user.mouse_control_chicken_set_line_color(mouse_control_chicken_color_name)
chicken line (transparency|transparent) <user.mouse_control_chicken_percentage>:
    user.mouse_control_chicken_set_line_transparency(mouse_control_chicken_percentage)

chicken quick [(act|action)] [on]: user.mouse_control_chicken_enable_quick_action_context()
chicken quick [(act|action)] off: user.mouse_control_chicken_disable_quick_action_context()

chicken {user.mouse_control_chicken_number_small}:
    user.mouse_control_chicken_update_numeric_grid_parameters(mouse_control_chicken_number_small)
chicken {user.mouse_control_chicken_number_small} {user.mouse_control_chicken_number_small}:
    user.mouse_control_chicken_update_numeric_grid_parameters(mouse_control_chicken_number_small, mouse_control_chicken_number_small_2)

