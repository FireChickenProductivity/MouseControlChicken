from talon import Context
from .ContextUtilities import create_context_matches_single_tag_string
from .TagManagement import GRID_CREATION_ARGUMENT_POSITIVE_INTEGER_TAG
from .GridFactoryArgumentTypes import CAPTURE_NAME

positive_integer_context = Context()
positive_integer_context.matches = create_context_matches_single_tag_string(GRID_CREATION_ARGUMENT_POSITIVE_INTEGER_TAG)

@positive_integer_context.capture(CAPTURE_NAME, rule = '<number_small>')
def mouse_control_chicken_grid_factory_argument(m) -> str:
    return m[0]