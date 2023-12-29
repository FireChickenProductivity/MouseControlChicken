from talon import Context
from .ContextUtilities import create_context_matches_single_tag_string
from .TagManagement import GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG
from .GridFactoryArgumentTypes import CAPTURE_NAME

two_to_nine_context = Context()
two_to_nine_context.matches = create_context_matches_single_tag_string(GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG)

@two_to_nine_context.capture(CAPTURE_NAME, rule = "two|three|four|five|six|seven|eight|nine")
def mouse_control_chicken_grid_factory_argument(m) -> str:
    number_text = m[0]
    if number_text == "two":
        return "2"
    elif number_text == "three":
        return "3"
    elif number_text == "four":
        return "4"
    elif number_text == "five":
        return "5"
    elif number_text == "six":
        return "6"
    elif number_text == "seven":
        return "7"
    elif number_text == "eight":
        return "8"
    elif number_text == "nine":
        return "9"
    else:
        return ""