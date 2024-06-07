from talon import Module, settings, app
from .SettingsFileManagement import create_settings_file
from .SettingsCreation import SettingCreator
from .Callbacks import CallbackManager, Callback

module = Module()

setting_creator = SettingCreator(module)

default_grid_option = setting_creator.create_str_setting(
    'default_grid_option',
    default = "double alphabet numbers",
    desc = 'The default grid option used by Mouse Control Chicken',
)

default_text_size = setting_creator.create_int_setting(
    'default_text_size',
    default = 10,
    desc = 'The default text size used by Mouse Control Chicken'
) 

default_text_color = setting_creator.create_str_setting(
    'default_text_color',
    default = "66ff00",
    desc = 'The default text color used by Mouse Control Chicken'
) 

default_line_width = setting_creator.create_int_setting(
    'default_line_width',
    default = 1,
    desc = 'The default line width used by Mouse Control Chicken'
) 

default_line_color = setting_creator.create_str_setting(
    'default_line_color',
    default = "FF0000",
    desc = 'The default line color used by Mouse Control Chicken'
) 

default_background_transparency = setting_creator.create_float_setting(
    'default_background_transparency',
    default = 0.50,
    desc = 'The default background transparency used by Mouse Control Chicken'
)  

default_alternate_background_transparency = setting_creator.create_float_setting(
    'default_alternate_background_transparency',
    default = 0.75,
    desc = 'The default alternate background transparency used by Mouse Control Chicken when flickering to the alternate transparency setting'
)

default_background_color = setting_creator.create_str_setting(
    'default_background_color',
    default = "000000",
    desc = "The default background color used by Mouse Control Chicken"
)

default_main_transparency = setting_creator.create_float_setting(
    'default_main_transparency',
    default = 0,
    desc = 'The default main transparency used by Mouse Control Chicken'
) 

default_alternate_main_transparency = setting_creator.create_float_setting(
    'default_alternate_main_transparency',
    default = 0.66,
    desc= 'The default alternate main transparency used by Mouse Control Chicken when flickering to the alternate transparency setting'
)

default_current_screen_number = setting_creator.create_int_setting(
    'default_current_screen_number',
    default = 0,
    desc = 'The default screen number used by Mouse Control Chicken'
) 

default_frame_grid_offset = setting_creator.create_int_setting(
    'default_frame_grid_offset',
    default = 10,
    desc = 'The default frame grid offset used by Mouse Control Chicken. Determines how far from the frame the text is in a frame grid display.'
)

default_frame_grid_should_show_crisscross = setting_creator.create_bool_setting(
    'default_frame_grid_should_show_crisscross',
    default = False,
    desc = 'Determines whether or not mouse control chicken frame grids should show crisscross lines by default.'
)

default_checker_frequency = setting_creator.create_int_setting(
    'default_checker_frequency',
    3,
    'The default checker frequency used by Mouse Control Chicken. Every nth position is shown on a checker display where n is the frequency.'
)

default_zigzag_threshold = setting_creator.create_int_setting(
    'default_zigzag_threshold',
    0,
    'The default zigzag threshold used by Mouse Control Chicken. Determines how many positions are shown in a zigzagging display before the direction of the zigzag is reversed.'
)

scrolling_amount = setting_creator.create_int_setting(
    'scrolling_amount',
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

transparency_flickering_show_time = setting_creator.create_int_setting(
    'transparency_flickering_show_time',
    5000,
    'The amount of time that mouse control chicken transparency flickering will show a display with default transparency settings before alternating in milliseconds.'
)

transparency_flickering_hide_time = setting_creator.create_int_setting(
    'transparency_flickering_hide_time',
    2000,
    'The amount of time that mouse control chicken transparency flickering will hide a display with alternate transparency settings before alternating in milliseconds.'
)

default_rectangle_manager = setting_creator.create_str_setting(
    'default_rectangle_manager',
    'screen',
    'The default rectangle manager used by Mouse Control Chicken. Determines what to draw the grid around.'
)


class SettingsMediator:
    def __init__(self):
        self.callback_manager = CallbackManager()
        self.initialize()
        
    def initialize(self):
        self.restore_default_settings()
        self.initialize_persistent_settings()
    
    def initialize_persistent_settings(self):
       self.current_screen_number = settings.get(default_current_screen_number)
    
    def restore_transparency_settings(self):
        self.background_transparency = settings.get(default_background_transparency)
        self.main_transparency = settings.get(default_main_transparency)

    def initialize_flicker_time_settings(self):
        self.flickering_show_time = settings.get(flickering_show_time)
        self.flickering_hide_time = settings.get(flickering_hide_time)
        self.transparency_flickering_show_time = settings.get(transparency_flickering_show_time)
        self.transparency_flickering_hide_time = settings.get(transparency_flickering_hide_time)

    def restore_default_settings(self):
        self.default_grid_option = settings.get(default_grid_option)
        self.text_size = settings.get(default_text_size)
        self.text_color = settings.get(default_text_color)
        self.line_width = settings.get(default_line_width)
        self.line_color = settings.get(default_line_color)
        self.background_color = settings.get(default_background_color)
        self.frame_grid_offset = settings.get(default_frame_grid_offset)
        self.frame_grid_should_show_crisscross = settings.get(default_frame_grid_should_show_crisscross)
        self.checker_frequency = settings.get(default_checker_frequency)
        self.zigzag_threshold = settings.get(default_zigzag_threshold)
        self.flickering_enabled = settings.get(flickering_enabled)
        self.default_rectangle_manager = settings.get(default_rectangle_manager)
        self.alternate_background_transparency = settings.get(default_alternate_background_transparency)
        self.alternate_main_transparency = settings.get(default_alternate_main_transparency)
        self.initialize_flicker_time_settings()
        self.restore_transparency_settings()
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

    def get_zigzag_threshold(self) -> int:
        return self.zigzag_threshold

    def get_scrolling_amount(self) -> int:
        return settings.get(scrolling_amount)

    def get_flickering_enabled(self) -> bool:
        return self.flickering_enabled

    def get_flickering_show_time(self) -> int:
        return self.flickering_show_time

    def get_flickering_hide_time(self) -> int:
        return self.flickering_hide_time

    def get_transparency_flickering_show_time(self) -> int:
        return self.transparency_flickering_show_time
    
    def get_transparency_flickering_hide_time(self) -> int:
        return self.transparency_flickering_hide_time

    def get_default_rectangle_manager(self) -> str:
        return self.default_rectangle_manager
    
    def rotate_transparency_settings_to_alternates(self):
        self.background_transparency = self.alternate_background_transparency
        self.main_transparency = self.alternate_main_transparency

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

    def update_transparencies(self, background_transparency: float, main_transparency: float):
        self.background_transparency = background_transparency
        self.main_transparency = main_transparency

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

    def set_zigzag_threshold(self, threshold: int):
        self.zigzag_threshold = threshold
        self._handle_change()

    def register_on_change_callback(self, name: str, callback: Callback):
        self.callback_manager.register_callback(name, callback)
    
    def _handle_change(self):
        self.callback_manager.call_callbacks()

settings_mediator = SettingsMediator()
def load_default_settings():
    global settings_mediator
    settings_mediator.initialize()
    create_settings_file()
app.register('ready', load_default_settings)

@module.action_class
class Actions:
    def mouse_control_chicken_toggle_frame_display_crisscross():
        '''Toggles whether mouse control chicken frame displays should show  crisscrossing lines'''
        settings_mediator.set_frame_grid_should_show_crisscross(not settings_mediator.get_frame_grid_should_show_crisscross())

    def mouse_control_chicken_set_checker_frequency(frequency: int):
        '''Sets the mouse control chicken checker frequency'''
        settings_mediator.set_checker_frequency(frequency)

    def mouse_control_chicken_set_zigzag_threshold(threshold: int):
        '''Sets the mouse control chicken zigzag threshold'''
        settings_mediator.set_zigzag_threshold(threshold)

    def mouse_control_chicken_refresh():
        '''Refreshes the mouse control chicken grid and reloads settings from their defaults'''
        settings_mediator.restore_default_settings()