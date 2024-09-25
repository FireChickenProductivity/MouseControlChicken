-
chicken choose grid <user.mouse_control_chicken_grid_option>: 
    user.mouse_control_chicken_choose_grid_from_options(mouse_control_chicken_grid_option)

chicken hide: user.mouse_control_chicken_hide_grid()
chicken show: user.mouse_control_chicken_show_grid()

chicken choose grid: user.mouse_control_chicken_show_grid_options()
chicken choose display: user.mouse_control_chicken_show_display_options()
chicken choose default display: user.mouse_control_chicken_show_default_display_options()

chicken [screen] next: 
    user.mouse_control_chicken_use_next_screen()
    user.mouse_control_chicken_set_rectangle_manager_to_screen()
chicken [screen] last: 
    user.mouse_control_chicken_use_previous_screen()
    user.mouse_control_chicken_set_rectangle_manager_to_screen()
chicken screen <number_small>: 
    user.mouse_control_chicken_use_screen(number_small)
    user.mouse_control_chicken_set_rectangle_manager_to_screen()
chicken (window|dough|when): user.mouse_control_chicken_set_rectangle_manager_to_window()
chicken follow (window|dough|when): user.mouse_control_chicken_set_rectangle_manager_to_follow_window()
chicken follow screen: user.mouse_control_chicken_set_rectangle_manager_to_follow_screen()
chicken refresh: user.mouse_control_chicken_refresh()

chicken down [<number_small>]:
    user.mouse_control_chicken_start_scrolling(number_small or 1)

chicken up [<number_small>]:
    user.mouse_control_chicken_start_scrolling(number_small or 1, false)