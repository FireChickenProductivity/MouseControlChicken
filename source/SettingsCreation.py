from talon import Module

class SettingCreator:
    def __init__(self, module: Module):
        self.module = module
    
    def compute_setting_name_with_prefix(self, name: str) -> str:
        return 'mouse_control_chicken_' + name

    def compute_setting_string(self, name: str) -> str:
        return 'user.' + self.compute_setting_name_with_prefix(name)
    
    def _create_setting(self, name: str, setting_type, default, desc: str):
        self.module.setting(
            self.compute_setting_name_with_prefix(name),
            type = setting_type,
            default = default,
            desc = desc
        )
        return self.compute_setting_string(name)

    def create_bool_setting(self, name: str, default: bool, desc: str):
        return self._create_setting(name, bool, default, desc)
    
    def create_int_setting(self, name: str, default: int, desc: str):
        return self._create_setting(name, int, default, desc)

    def create_float_setting(self, name: str, default: float, desc: str):
        return self._create_setting(name, float, default, desc)

    def create_str_setting(self, name: str, default: str, desc: str):
        return self._create_setting(name, str, default, desc)

