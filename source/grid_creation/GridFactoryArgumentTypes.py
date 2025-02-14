#This module defines classes for understanding arguments that can be passed to grid factories. This is used to generate an appropriate user interface for creating custom grids.
#Note: Argument type tags should only be provided when an argument as being handled through a custom override of the dictation input capture. These are not needed for working with the options dialogue, which is done through its own tag and context for overriding the dictation input capture and instead requires returning true for supports_options_dialogue.

from ..TagManagement import GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG, ARGUMENT_INPUT_THROUGH_DICTATION_INPUT_TAG \
, GRID_CREATION_ARGUMENT_POSITIVE_INTEGER_TAG
from ..GridOptionsList import get_grid_options
from ..dialogue.DictationInputDialogue import DICTATION_INPUT_CAPTURE
from ..ContextUtilities import create_context_matches_single_tag_string
from talon import actions, Context, Module
from typing import List


class OptionsNotSupportedException(Exception): pass

class InvalidFactoryArgumentException(Exception): pass

class FactoryArgumentType:
    def does_argument_match_type(self, argument):
        try:
            converted_value = self.convert_argument(argument)
        except:
            return False
        return self._argument_has_valid_value(converted_value)

    def _argument_has_valid_value(self, argument):
        pass

    def get_tags(self) -> List[str]:
        pass

    def supports_options_dialogue(self) -> bool:
        pass

    def get_options(self) -> List[str]:
        pass

class TagBasedFactoryArgumentType(FactoryArgumentType):
    def __init__(self, type: type, tag: str, has_valid_value):
        self.type = type
        self.tag = tag
        self.has_valid_value = has_valid_value
   
    def convert_argument(self, argument):
        return self.type(argument)

    def _argument_has_valid_value(self, argument):
        return self.has_valid_value(argument)

    def get_tags(self) -> List[str]:
        #Avoid overriding the dictation input capture through a tag when using the options dialogue because it uses its own tag and context to override that already
        tags = [ARGUMENT_INPUT_THROUGH_DICTATION_INPUT_TAG, self.tag]
        return tags

    def supports_options_dialogue(self) -> bool:
        return False

    def get_options(self) -> List[str]:
        raise OptionsNotSupportedException()

class TwoToNineArgumentType(TagBasedFactoryArgumentType):
    def __init__(self):
        super().__init__(
            int,
            GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG,
            lambda argument: argument >= 2 and argument <= 9 
        )
    
class PositiveIntegerArgumentType(TagBasedFactoryArgumentType):
    def __init__(self):
        super().__init__(
            int,
            GRID_CREATION_ARGUMENT_POSITIVE_INTEGER_TAG,
            lambda argument: argument > 0
        )
        
class OptionsBasedFactoryArgumentType(FactoryArgumentType):
    def __init__(self, has_valid_value, compute_options):
        self.has_valid_value = has_valid_value
        self.compute_options = compute_options

    def convert_argument(self, argument):
        return str(argument)

    def _argument_has_valid_value(self, argument):
        return self.has_valid_value(argument)

    def supports_options_dialogue(self) -> bool:
        return True
    
    def get_options(self) -> List[str]:
        return self.compute_options()

    def get_tags(self) -> List[str]:
        return []

class GridOptionArgumentType(OptionsBasedFactoryArgumentType):
    def __init__(self):
        super().__init__(
            lambda argument: get_grid_options().
                                has_option(argument),
            lambda: get_grid_options().
                        get_option_names()
        )

class CustomCoordinateSystemArgumentType(OptionsBasedFactoryArgumentType):
    def __init__(self):
        super().__init__(
            actions.user.mouse_control_chicken_coordinate_list_file_exists,
            actions.user.mouse_control_chicken_compute_coordinate_list_file_names
        )

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