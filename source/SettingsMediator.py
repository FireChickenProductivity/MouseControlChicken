from talon import Module, settings, app

module = Module()

default_grid_option_setting_name = 'mouse_control_chicken_default_grid_option'
default_grid_option = 'user.' + default_grid_option_setting_name
module.setting(
    default_grid_option_setting_name,
    type = str,
    default = "double alphabet numbers",
    desc = 'The default grid option used by Mouse Control Chicken',
)

default_text_size_setting_name = 'mouse_control_chicken_default_text_size'
default_text_size = 'user.' + default_text_size_setting_name
module.setting(
    default_text_size_setting_name,
    type = int,
    default = 10,
    desc = 'The default text size used by Mouse Control Chicken'
) 

default_text_color_setting_name = 'mouse_control_chicken_default_text_color'
default_text_color = 'user.' + default_text_color_setting_name
module.setting(
    default_text_color_setting_name,
    type = str,
    default = "66ff00",
    desc = 'The default text color used by Mouse Control Chicken'
) 

default_line_width_setting_name = 'mouse_control_chicken_default_line_width'
default_line_width = 'user.' + default_line_width_setting_name
module.setting(
    default_line_width_setting_name,
    type = int,
    default = 2,
    desc = 'The default line width used by Mouse Control Chicken'
) 

default_line_color_setting_name = 'mouse_control_chicken_default_line_color'
default_line_color = 'user.' + default_line_color_setting_name
module.setting(
    default_line_color_setting_name,
    type = str,
    default = "FF0000",
    desc = 'The default line color used by Mouse Control Chicken'
) 

default_background_transparency_setting_name = 'mouse_control_chicken_default_background_transparency'
default_background_transparency = 'user.' + default_background_transparency_setting_name
module.setting(
    default_background_transparency_setting_name,
    type = float,
    default = 0.50,
    desc = 'The default background transparency used by Mouse Control Chicken'
)  

default_background_color_setting_name = 'mouse_control_chicken_default_background_color'
default_background_color = 'user.' + default_background_color_setting_name
module.setting(
    default_background_color_setting_name,
    type = str,
    default = "000000",
    desc = "The default background color used by Mouse Control Chicken"
)

default_main_transparency_setting_name = 'mouse_control_chicken_default_main_transparency'
default_main_transparency = 'user.' + default_main_transparency_setting_name
module.setting(
    default_main_transparency_setting_name,
    type = float,
    default = 0.3,
    desc = 'The default main transparency used by Mouse Control Chicken'
) 

default_current_screen_number_setting_name = 'mouse_control_chicken_default_current_screen_number'
default_current_screen_number = 'user.' + default_current_screen_number_setting_name
module.setting(
    default_current_screen_number_setting_name,
    type = int,
    default = 0,
    desc = 'The default screen number used by Mouse Control Chicken'
) 

default_frame_grid_offset_setting_name = 'mouse_control_chicken_default_frame_grid_offset'
default_frame_grid_offset = 'user.' + default_frame_grid_offset_setting_name
module.setting(
    default_frame_grid_offset_setting_name,
    type = int,
    default = 10,
    desc = 'The default frame grid offset used by Mouse Control Chicken. Determines how far from the frame the text is in a frame grid display.'
)

default_frame_grid_should_show_crisscross_setting_name = 'mouse_control_chicken_default_frame_grid_should_show_crisscross'
default_frame_grid_should_show_crisscross = 'user.' + default_frame_grid_should_show_crisscross_setting_name
module.setting(
    default_frame_grid_should_show_crisscross_setting_name,
    type = bool,
    default = False,
    desc = 'Determines whether or not mouse control chicken frame grids should show crisscross lines by default.'
)

class SettingsMediator:
    def __init__(self):
        self.callbacks = []
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

    def register_on_change_callback(self, callback):
        self.callbacks.append(callback)
    
    def _handle_change(self):
        for callback in self.callbacks: callback()

settings_mediator = SettingsMediator()
def load_default_settings():
    global settings_mediator
    settings_mediator.restore_default_settings()

app.register('ready', load_default_settings)