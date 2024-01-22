from talon import Module, settings, app
from .file_management.FileUtilities import write_text_to_file_if_uninitialized, compute_path_within_output_directory
from .Callbacks import CallbackManager, Callback

module = Module()

def create_setting(module: Module, name: str, setting_type, default, desc: str):
    setting_name = 'mouse_control_chicken_' + name
    setting = 'user.' + setting_name
    module.setting(
        setting_name,
        type = setting_type,
        default = default,
        desc = desc
    )
    return setting

class SettingCreator:
    def __init__(self, module: Module):
        self.module = module
    
    def compute_setting_name_with_prefix(self, name: str) -> str:
        return 'mouse_control_chicken_' + name

    def compute_setting_string(self, name: str) -> str:
        return 'user.' + self.compute_setting_name_with_prefix(name)
    
    def create_bool_setting(self, name: str, default: bool, desc: str):
        self.module.setting(
            self.compute_setting_name_with_prefix(name),
            type = bool,
            default = default,
            desc = desc
        )
        return self.compute_setting_string(name)
    
    def create_int_setting(self, name: str, default: int, desc: str):
        self.module.setting(
            self.compute_setting_name_with_prefix(name),
            type = int,
            default = default,
            desc = desc
        )
        return self.compute_setting_string(name)
setting_creator = SettingCreator(module)

default_grid_option_setting_name = 'default_grid_option'
default_grid_option = create_setting(
    module,
    'default_grid_option',
    setting_type = str,
    default = "double alphabet numbers",
    desc = 'The default grid option used by Mouse Control Chicken',
)

default_text_size_setting_name = 'default_text_size'
default_text_size = create_setting(
    module,
    'default_text_size',
    setting_type = int,
    default = 10,
    desc = 'The default text size used by Mouse Control Chicken'
) 

default_text_color_setting_name = 'default_text_color'
default_text_color = create_setting(
    module,
    'default_text_color',
    setting_type = str,
    default = "66ff00",
    desc = 'The default text color used by Mouse Control Chicken'
) 

default_line_width_setting_name = 'default_line_width'
default_line_width = create_setting(
    module,
    'default_line_width',
    setting_type = int,
    default = 1,
    desc = 'The default line width used by Mouse Control Chicken'
) 

default_line_color_setting_name = 'default_line_color'
default_line_color = create_setting(
    module,
    'default_line_color',
    setting_type = str,
    default = "FF0000",
    desc = 'The default line color used by Mouse Control Chicken'
) 

default_background_transparency_setting_name = 'default_background_transparency'
default_background_transparency = create_setting(
    module,
    'default_background_transparency',
    setting_type = float,
    default = 0.50,
    desc = 'The default background transparency used by Mouse Control Chicken'
)  

default_background_color_setting_name = 'default_background_color'
default_background_color = create_setting(
    module,
    'default_background_color',
    setting_type = str,
    default = "000000",
    desc = "The default background color used by Mouse Control Chicken"
)

default_main_transparency_setting_name = 'default_main_transparency'
default_main_transparency = create_setting(
    module,
    'default_main_transparency',
    setting_type = float,
    default = 0,
    desc = 'The default main transparency used by Mouse Control Chicken'
) 

default_current_screen_number_setting_name = 'default_current_screen_number'
default_current_screen_number = create_setting(
    module,
    'default_current_screen_number',
    setting_type = int,
    default = 0,
    desc = 'The default screen number used by Mouse Control Chicken'
) 

default_frame_grid_offset_setting_name = 'default_frame_grid_offset'
default_frame_grid_offset = create_setting(
    module,
    'default_frame_grid_offset',
    setting_type = int,
    default = 10,
    desc = 'The default frame grid offset used by Mouse Control Chicken. Determines how far from the frame the text is in a frame grid display.'
)

default_frame_grid_should_show_crisscross_setting_name = 'default_frame_grid_should_show_crisscross'
default_frame_grid_should_show_crisscross = create_setting(
    module,
    'default_frame_grid_should_show_crisscross',
    setting_type = bool,
    default = False,
    desc = 'Determines whether or not mouse control chicken frame grids should show crisscross lines by default.'
)

default_checker_frequency = create_setting(
    module,
    'default_checker_frequency',
    int,
    3,
    'The default checker frequency used by Mouse Control Chicken. Every nth position is shown on a checker display where n is the frequency.'
)

scrolling_amount = create_setting(
    module,
    'scrolling_amount',
    int,
    600,
    'The amount that mouse control chicken standard scrolling commands will scroll.'
)

flickering_enabled = setting_creator.create_bool_setting(
    'flickering_enabled',
    False,
    'Whether or not mouse control chicken flickering is enabled.'
)

flickering_show_time = setting_creator.create_int_setting(
    'flickering_show_time',
    5000,
    'The amount of time that mouse control chicken flickering will show a display for before hiding it in milliseconds.'
)

flickering_hide_time = setting_creator.create_int_setting(
    'flickering_hide_time',
    2000,
    'The amount of time that mouse control chicken flickering will hide a display for before showing it in milliseconds.'   
)

class SettingsMediator:
    def __init__(self):
        self.callback_manager = CallbackManager()
        self.restore_default_settings()
    
    def restore_default_settings(self):
        self.default_grid_option = settings.get(default_grid_option)
        self.text_size = settings.get(default_text_size)
        self.text_color = settings.get(default_text_color)
        self.line_width = settings.get(default_line_width)
        self.line_color = settings.get(default_line_color)
        self.background_transparency = settings.get(default_background_transparency)
        self.background_color = settings.get(default_background_color)
        self.main_transparency = settings.get(default_main_transparency)
        self.current_screen_number = settings.get(default_current_screen_number)
        self.frame_grid_offset = settings.get(default_frame_grid_offset)
        self.frame_grid_should_show_crisscross = settings.get(default_frame_grid_should_show_crisscross)
        self.checker_frequency = settings.get(default_checker_frequency)
        self.flickering_enabled = settings.get(flickering_enabled)
        self.flickering_show_time = settings.get(flickering_show_time)
        self.flickering_hide_time = settings.get(flickering_hide_time)
        self._handle_change()

    def get_default_grid_option(self) -> str:
        return self.default_grid_option

    def get_text_size(self) -> int:
        return self.text_size

    def get_text_color(self) -> str:
        return self.text_color

    def get_line_width(self) -> int:
        return self.line_width

    def get_line_color(self) -> str:
        return self.line_color

    def get_background_transparency(self) -> float:
        return self.background_transparency

    def get_background_color(self) -> str:
        return self.background_color

    def get_main_transparency(self) -> float:
        return self.main_transparency

    def get_current_screen_number(self) -> int:
        return self.current_screen_number

    def get_frame_grid_offset(self) -> int:
        return self.frame_grid_offset

    def get_frame_grid_should_show_crisscross(self) -> bool:
        return self.frame_grid_should_show_crisscross

    def get_checker_frequency(self) -> int:
        return self.checker_frequency

    def get_scrolling_amount(self) -> int:
        return settings.get(scrolling_amount)

    def get_flickering_enabled(self) -> bool:
        return self.flickering_enabled

    def get_flickering_show_time(self) -> int:
        return self.flickering_show_time

    def get_flickering_hide_time(self) -> int:
        return self.flickering_hide_time

    def set_text_size(self, size: int):
        self.text_size = size
        self._handle_change()

    def set_text_color(self, color: str):
        self.text_color = color
        self._handle_change()

    def set_line_width(self, width: int):
        self.line_width = width
        self._handle_change()

    def set_line_color(self, color: str):
        self.line_color = color
        self._handle_change()

    def set_background_transparency(self, transparency: float):
        self.background_transparency = transparency
        self._handle_change()
    
    def set_background_color(self, color: str):
        self.background_color = color
        self._handle_change()

    def set_main_transparency(self, transparency: float):
        self.main_transparency = transparency
        self._handle_change()

    def set_current_screen_number(self, number: int):
        self.current_screen_number = number
        self._handle_change()

    def set_frame_grid_offset(self, offset: int):
        self.frame_grid_offset = offset
        self._handle_change()

    def set_frame_grid_should_show_crisscross(self, should_show: bool):
        self.frame_grid_should_show_crisscross = should_show
        self._handle_change()

    def set_checker_frequency(self, frequency: int):
        self.checker_frequency = frequency
        self._handle_change()

    def register_on_change_callback(self, name: str, callback: Callback):
        self.callback_manager.register_callback(name, callback)
    
    def _handle_change(self):
        self.callback_manager.call_callbacks()

settings_mediator = SettingsMediator()
def load_default_settings():
    global settings_mediator
    settings_mediator.restore_default_settings()
    create_settings_file()

def create_settings_file():
    path = compute_path_within_output_directory("settings.talon")
    write_text_to_file_if_uninitialized(
        path,
        r"""-
settings():
    #The name of the default grid option. This must be one of the great options that shows up when you open the grid options list.
    user.mouse_control_chicken_default_grid_option = "double alphabet numbers"
    user.mouse_control_chicken_default_text_size = 10
    user.mouse_control_chicken_default_text_color = "66ff00"
    user.mouse_control_chicken_default_line_width = 1
    user.mouse_control_chicken_default_line_color = "FF0000"
    user.mouse_control_chicken_default_background_transparency = 0.50
    user.mouse_control_chicken_default_background_color = "000000"
    user.mouse_control_chicken_default_main_transparency = 0
    #This determines the default screen that the grid will be shown on.
    user.mouse_control_chicken_default_current_screen_number = 0
    #This determines how far from the frame the text is in a frame grid display.
    user.mouse_control_chicken_default_frame_grid_offset = 10
    user.mouse_control_chicken_default_frame_grid_should_show_crisscross = false
    #Every nth position is shown on a checker display where n is the frequency.
    user.mouse_control_chicken_default_checker_frequency = 3
    user.mouse_control_chicken_scrolling_amount = 600
    user.mouse_control_chicken_flickering_enabled = false
    user.mouse_control_chicken_flickering_show_time = 5000
    user.mouse_control_chicken_flickering_hide_time = 2000
"""

    )

app.register('ready', load_default_settings)

@module.action_class
class Actions:
    def mouse_control_chicken_toggle_frame_display_crisscross():
        '''Toggles whether mouse control chicken frame displays should show  crisscrossing lines'''
        settings_mediator.set_frame_grid_should_show_crisscross(not settings_mediator.get_frame_grid_should_show_crisscross())

    def mouse_control_chicken_set_checker_frequency(frequency: int):
        '''Sets the mouse control chicken checker frequency'''
        settings_mediator.set_checker_frequency(frequency)

    def mouse_control_chicken_refresh():
        '''Refreshes the mouse control chicken grid and reloads settings from their defaults'''
        settings_mediator.restore_default_settings()