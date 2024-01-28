from talon import Context
from .ContextUtilities import create_context_matches_single_tag_string
from .TagManagement import GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG
from .GridFactoryArgumentTypes import CAPTURE_NAME

two_to_nine_context = Context()
two_to_nine_context.matches = create_context_matches_single_tag_string(GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG)

@two_to_nine_context.capture(CAPTURE_NAME, rule = "two|three|four|five|six|seven|eight|nine")
def mouse_control_chicken_grid_factory_argument(m) -> str:
    number_text = m[0]
    result: str = ""
    if number_text == "two":
        result = "2"
    elif number_text == "three":
        result = "3"
    elif number_text == "four":
        result = "4"
    elif number_text == "five":
        result = "5"
    elif number_text == "six":
        result = "6"
    elif number_text == "seven":
        result = "7"
    elif number_text == "eight":
        result = "8"
    elif number_text == "nine":
        result = "9"
    return result