from .TagManagement import GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG, GRID_CREATION_ARGUMENT_GRID_OPTION_TAG, ARGUMENT_INPUT_THROUGH_DICTATION_INPUT_TAG
from .dialogue.DictationInputDialogue import DICTATION_INPUT_CAPTURE
from .ContextUtilities import create_context_matches_single_tag_string
from .GridOptions import GridOptions
from talon import actions, Context, Module
from typing import List


class OptionsNotSupportedException(Exception): pass

class InvalidFactoryArgumentException(Exception): pass

class FactoryArgumentType:
    def __init__(self, type: type, tag: str):
        self.type = type
        self.tag = tag
    
    def does_argument_match_type(self, argument):
        try:
            converted_value = self.convert_argument(argument)
        except:
            return False
        return self._argument_has_valid_value(converted_value)
    
    def convert_argument(self, argument):
        return self.type(argument)

    def _argument_has_valid_value(self, argument):
        pass

    def get_tag(self) -> str:
        return self.tag

    def get_tags(self) -> List[str]:
        return [self.get_tag(), ARGUMENT_INPUT_THROUGH_DICTATION_INPUT_TAG]

    def supports_options_dialogue(self) -> bool:
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
        options: GridOptions = actions.user.mouse_control_chicken_get_grid_options()
        return options.has_option(argument)

    def supports_options_dialogue(self) -> bool:
        return True

    def get_options(self) -> List[str]:
        options: GridOptions = actions.user.mouse_control_chicken_get_grid_options()
        return options.get_option_names()

CAPTURE_NAME = "user.mouse_control_chicken_grid_factory_argument"
module = Module()
@module.capture(rule = "placeholder")
def mouse_control_chicken_grid_factory_argument(m) -> str:
    return ""

context = Context()
context.matches = create_context_matches_single_tag_string(ARGUMENT_INPUT_THROUGH_DICTATION_INPUT_TAG)
@context.capture(DICTATION_INPUT_CAPTURE, rule = f"<user.mouse_control_chicken_grid_factory_argument>")
def mouse_control_chicken_dictation_input(m) -> str:
    return m.mouse_control_chicken_grid_factory_argument