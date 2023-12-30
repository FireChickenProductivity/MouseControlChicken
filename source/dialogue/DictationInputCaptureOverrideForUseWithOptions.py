from .DictationInputDialogue import DICTATION_INPUT_CAPTURE
from ..ContextUtilities import create_context_matches_single_tag_string
from ..TagManagement import DICTATION_INPUT_WITH_OPTIONS_TAG
from talon import Context

context = Context()
context.matches = create_context_matches_single_tag_string(DICTATION_INPUT_WITH_OPTIONS_TAG)

@context.capture(DICTATION_INPUT_CAPTURE, rule = "<number_small>")
def mouse_control_chicken_dictation_input(m) -> int:
    return m.number_small