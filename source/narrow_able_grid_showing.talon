tag: user.mouse_control_chicken_narrow_able_showing
mode: user.mouse_control_chicken_narrow_able_grid_mode
mode: command
-

reset: 
    user.mouse_control_chicken_reset_narrow_able_grid()

tap here: user.mouse_control_chicken_click_current_position_on_narrow_able_grid()

pierce here: user.mouse_control_chicken_double_click_current_position_on_narrow_able_grid()

brush here: user.mouse_control_chicken_right_click_current_position_on_narrow_able_grid()

hold here: user.mouse_control_chicken_drag_from_current_position_on_narrow_able_grid()

drop here: user.mouse_control_chicken_end_drag_at_current_position_on_narrow_able_grid()

meet here: user.mouse_control_chicken_move_mouse_to_position_on_narrow_able_grid()

twist here: user.mouse_control_chicken_scroll_up_at_current_position_on_narrow_able_grid()

roll here: user.mouse_control_chicken_scroll_down_at_current_position_on_narrow_able_grid()

down here [speed <number_small>]: 
    user.mouse_control_chicken_start_scrolling_at_current_position_on_narrow_able_grid(number_small or 1)

up here [speed <number_small>]:
    user.mouse_control_chicken_start_scrolling_at_current_position_on_narrow_able_grid(number_small or 1, false)