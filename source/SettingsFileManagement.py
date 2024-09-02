from .file_management.FileUtilities import compute_path_within_output_directory
import os
from typing import List
from talon import app

class SettingsFileEntry:
    def __init__(self, name, value, comment_lines = None):
        self.name = name
        self.value = value
        self.comment_lines = comment_lines
        if not self.comment_lines:
            self.comment_lines = []
    
    def compute_text(self) -> str:
        result = ""
        for line in self.comment_lines:
            result += f"\t#{line}\n"
        result += f"\t{self.name} = {self.value}"
        return result

    def get_name(self) -> str:
        return self.name

def compute_setting_name_from_line(line: str) -> str:
    if line.startswith("\t") and "=" in line:
        return line.split("=")[0].strip()
    return None

def compute_settings_already_in_settings_file(path: str):
    encountered_settings = set()
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines:
            name = compute_setting_name_from_line(line)
            if name: encountered_settings.add(name)
    return encountered_settings

def append_missing_settings_to_settings_file(path: str, missing_settings: List[SettingsFileEntry]):
    with open(path, "a") as file:
        for entry in missing_settings:
            file.write(entry.compute_text() + "\n")
            app.notify(f"Added missing setting {entry.get_name()} to settings.talon")

def append_any_missing_settings_to_settings_file(path: str, setting_file_entrees: List[SettingsFileEntry]):
    encountered_settings = compute_settings_already_in_settings_file(path)
    missing_settings = [entry for entry in setting_file_entrees if entry.get_name() not in encountered_settings]
    if missing_settings:
        append_missing_settings_to_settings_file(path, missing_settings)

def create_settings_file():
    path = compute_path_within_output_directory("settings.talon")
    setting_file_entrees = [
        SettingsFileEntry(
            "user.mouse_control_chicken_default_grid_option",
            "double alphabet numbers",
            ["The name of the default grid option. This must be one of the grid options that shows up when you open the grid options list."]
        ),
        SettingsFileEntry(
            "user.mouse_control_chicken_font",
            "lucida sans typewriter",
            ["The default font option makes it easier to differentiate between I and l.",
            "If you do not like it, you could try 'arial rounded mt', which is the default font used by the flex grid"]
        ),
        SettingsFileEntry("user.mouse_control_chicken_default_text_size", "10"),
        SettingsFileEntry("user.mouse_control_chicken_default_text_color", "66ff00"),
        SettingsFileEntry("user.mouse_control_chicken_default_line_width", "1"),
        SettingsFileEntry("user.mouse_control_chicken_default_line_color", "FF0000"),
        SettingsFileEntry("user.mouse_control_chicken_default_line_transparency", "0.5"),
        SettingsFileEntry("user.mouse_control_chicken_default_background_transparency", "0.50"),
        SettingsFileEntry("user.mouse_control_chicken_default_background_color", "000000"),
        SettingsFileEntry("user.mouse_control_chicken_default_main_transparency", "0"),
        SettingsFileEntry("user.mouse_control_chicken_default_current_screen_number", "0"),
        SettingsFileEntry("user.mouse_control_chicken_default_frame_grid_offset", "10"),
        SettingsFileEntry("user.mouse_control_chicken_default_frame_grid_should_show_crisscross", "false"),
        SettingsFileEntry("user.mouse_control_chicken_default_horizontal_frame_proximity_distance", "350"),
        SettingsFileEntry("user.mouse_control_chicken_default_vertical_frame_proximity_distance", "400"),
        SettingsFileEntry("user.mouse_control_chicken_default_checker_frequency", "3"),
        SettingsFileEntry("user.mouse_control_chicken_default_zigzag_threshold", "0"),
        SettingsFileEntry("user.mouse_control_chicken_scrolling_amount", "600"),
        SettingsFileEntry("user.mouse_control_chicken_flickering_enabled", "false"),
        SettingsFileEntry("user.mouse_control_chicken_flickering_show_time", "5000"),
        SettingsFileEntry("user.mouse_control_chicken_flickering_hide_time", "2000"),
        SettingsFileEntry("user.mouse_control_chicken_default_rectangle_manager", "'screen'"),
        SettingsFileEntry("user.mouse_control_chicken_default_alternate_background_transparency", "0.75"),
        SettingsFileEntry("user.mouse_control_chicken_default_alternate_main_transparency", "0.66"),
        SettingsFileEntry("user.mouse_control_chicken_transparency_flickering_show_time", "5000"),
        SettingsFileEntry("user.mouse_control_chicken_transparency_flickering_hide_time", "2000"),
        SettingsFileEntry(
            "user.mouse_control_chicken_quick_action",
            '""',
            ["Set this to user.mouse_control_chicken_move_only_to_position to only move the mouse to the position when the quick action is performed.", 
            "This can be any talon action that takes a string as an argument."]
        ),
    ]
    text = "-\nsettings():\n"
    for entry in setting_file_entrees:
        text += entry.compute_text() + "\n"
    if os.path.exists(path):
        append_any_missing_settings_to_settings_file(path, setting_file_entrees)
    else:
        with open(path, "w") as file:
            file.write(text)