tag: user.mouse_control_chicken_narrow_able_showing
not mode: user.mouse_control_chicken_narrow_able_grid_mode
and mode: Command
-

seek <user.mouse_control_chicken_coordinates>: 
    user.mouse_control_chicken_enable_narrow_able_grid_mode()
    user.mouse_control_chicken_narrow_grid(mouse_control_chicken_coordinates)