from .file_management.FileUtilities import write_text_to_file_if_uninitialized, compute_path_within_output_directory

def create_settings_file():
    path = compute_path_within_output_directory("settings.talon")
    write_text_to_file_if_uninitialized(
        path,
        r"""-
settings():
    #The name of the default grid option. This must be one of the great options that shows up when you open the grid options list.
    user.mouse_control_chicken_default_grid_option = "double alphabet numbers"
    #The default font option makes it easier to differentiate between I and l.
    #If you do not like it, you could try "arial rounded mt", which is the default font used by the flex grid
    user.mouse_control_chicken_font = "lucida sans typewriter"
    user.mouse_control_chicken_default_text_size = 10
    user.mouse_control_chicken_default_text_color = "66ff00"
    user.mouse_control_chicken_default_line_width = 1
    user.mouse_control_chicken_default_line_color = "FF0000"
    user.mouse_control_chicken_default_line_transparency = 0.5
    user.mouse_control_chicken_default_background_transparency = 0.50
    user.mouse_control_chicken_default_background_color = "000000"
    user.mouse_control_chicken_default_main_transparency = 0
    #This determines the default screen that the grid will be shown on.
    user.mouse_control_chicken_default_current_screen_number = 0
    #This determines how far from the frame the text is in a frame grid display.
    user.mouse_control_chicken_default_frame_grid_offset = 10
    user.mouse_control_chicken_default_frame_grid_should_show_crisscross = false
    user.mouse_control_chicken_default_horizontal_frame_proximity_distance = 350
    user.mouse_control_chicken_default_vertical_frame_proximity_distance = 400
    #Every nth position is shown on a checker display where n is the frequency.
    user.mouse_control_chicken_default_checker_frequency = 3
    user.mouse_control_chicken_default_zigzag_threshold = 0
    user.mouse_control_chicken_scrolling_amount = 600
    user.mouse_control_chicken_flickering_enabled = false
    user.mouse_control_chicken_flickering_show_time = 5000
    user.mouse_control_chicken_flickering_hide_time = 2000
    user.mouse_control_chicken_default_rectangle_manager = 'screen'
    user.mouse_control_chicken_default_alternate_background_transparency = 0.75
    user.mouse_control_chicken_default_alternate_main_transparency = 0.66
    user.mouse_control_chicken_transparency_flickering_show_time = 5000
    user.mouse_control_chicken_transparency_flickering_hide_time = 2000
"""

    )