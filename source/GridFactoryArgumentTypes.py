from .TagManagement import GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG, GRID_CREATION_ARGUMENT_GRID_OPTION_TAG
from .GridOptions import GridOptions
from talon import actions
from typing import List


class OptionsNotSupportedException(Exception): pass

class FactoryArgumentType:
    def __init__(self, type: type, tag: str):
        self.type = type
        self.tag = tag
    
    def does_argument_match_type(self, argument):
        return isinstance(argument, self.type) and self._argument_has_valid_value(argument)
    
    def _argument_has_valid_value(self, argument):
        pass

    def get_tag(self) -> str:
        return self.tag

    def supports_options_display(self) -> bool:
        return False

    def get_options(self) -> List[str]:
        raise OptionsNotSupportedException()

class TwoToNineArgumentType(FactoryArgumentType):
    def __init__(self):
        super().__init__(int, GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG)
    
    def _argument_has_valid_value(self, argument):
        return argument >= 2 and argument <= 9
    
class GridOptionArgumentType(FactoryArgumentType):
    def __init__(self):
        super().__init__(str, GRID_CREATION_ARGUMENT_GRID_OPTION_TAG)

    def _argument_has_valid_value(self, argument):
        options: self.get_options()
        return options.has_option(argument)

    def supports_options_display(self) -> bool:
        return True

    def get_options(self) -> List[str]:
        options: GridOptions = actions.user.mouse_control_chicken_get_grid_options()
        return options.get_option_names()