tag: user.mouse_control_chicken_narrow_able_showing
mode: user.mouse_control_chicken_narrow_able_grid_mode
mode: command
-
reset: 
    user.mouse_control_chicken_reset_narrow_able_grid()

meet here: user.mouse_control_chicken_move_mouse_to_position_on_narrow_able_grid()

[<user.modifiers>] {user.mouse_control_chicken_action} here:
    user.mouse_control_chicken_perform_action_at_current_position_on_narrow_able_grid(mouse_control_chicken_action, modifiers or "")

down here [speed <number_small>]: 
    user.mouse_control_chicken_start_scrolling_at_current_position_on_narrow_able_grid(number_small or 1)

up here [speed <number_small>]:
    user.mouse_control_chicken_start_scrolling_at_current_position_on_narrow_able_grid(number_small or 1, false)