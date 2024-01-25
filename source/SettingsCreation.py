from talon import Module

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

    def create_float_setting(self, name: str, default: float, desc: str):
        self.module.setting(
            self.compute_setting_name_with_prefix(name),
            type = float,
            default = default,
            desc = desc
        )
        return self.compute_setting_string(name)

    def create_str_setting(self, name: str, default: str, desc: str):
        self.module.setting(
            self.compute_setting_name_with_prefix(name),
            type = str,
            default = default,
            desc = desc
        )
        return self.compute_setting_string(name)   

