#This defines the capture for dictating mouse control chicken coordinates
#This requires defining numerous sub captures to be used in the main capture based on the context
#This is complicated by the need to support grid composition. This is addressed by defining a context for each level of the grid

from talon import Module, Context, actions
from .InputCoordinateSystem import InputCoordinateSystem, InputCoordinateSystemCategory
from ..grid.Grid import Grid
from ..grid.GridCalculations import Node, compute_grid_tree, TreeComputationOptions
from .Captures import compute_coordinates_from_utterance
from .DepthCaptures import DEPTH_LIMIT, compute_level_tag
from .CustomCoordinates import CustomCoordinatesCaptureContext, create_base_custom_coordinate_system_capture_rule, create_pair_custom_coordinate_system_capture_rule, create_sequence_custom_coordinate_system_capture_rule
from .CoordinatesContext import CoordinateContext
from .CoordinateSystemTreeCalculations import compute_categories

module = Module()

default_context = Context()


CUSTOM_COORDINATE_SYSTEM_TAG_BASE_NAME = "mouse_control_chicken_custom_coordinates"
CUSTOM_COORDINATE_SYSTEM_PAIR_TAG_BASE_NAME = "mouse_control_chicken_custom_coordinates_pair"
CUSTOM_COORDINATE_SYSTEM_SEQUENCE_TAG_BASE_NAME = "mouse_control_chicken_custom_coordinates_sequence"


override_contexts = []
def build_override_contexts():
    input_coordinate_capture_names = ["mouse_control_chicken_number_sequence", "mouse_control_chicken_lowercase_letter_pair", "mouse_control_chicken_letter_pair", "mouse_control_chicken_single_number"]
    captures_to_override_by_level = {1:"mouse_control_chicken_main_coordinates", 2:"mouse_control_chicken_secondary_coordinates", 3:"mouse_control_chicken_tertiary_coordinates"}
    for input_coordinate_capture_name in input_coordinate_capture_names:
        for level, capture_to_override in captures_to_override_by_level.items():
            context = CoordinateContext(input_coordinate_capture_name, level)
            @context.context.capture("user." + capture_to_override, rule = f"<user.{input_coordinate_capture_name}>")
            def new_capture(m) -> str:
                text_list = [str(e) for e in m]
                return " ".join(text_list)
            module.tag(context.tag, desc=f"Tag for the level {level} of the {input_coordinate_capture_name} capture")
            override_contexts.append(context)
    
    custom_coordinate_captures = []
    for level in range(1, DEPTH_LIMIT + 1):
        base_context = CustomCoordinatesCaptureContext(CUSTOM_COORDINATE_SYSTEM_TAG_BASE_NAME, create_base_custom_coordinate_system_capture_rule(level), level)
        pair_context = CustomCoordinatesCaptureContext(CUSTOM_COORDINATE_SYSTEM_PAIR_TAG_BASE_NAME, create_pair_custom_coordinate_system_capture_rule(level), level)
        sequence_context = CustomCoordinatesCaptureContext(CUSTOM_COORDINATE_SYSTEM_SEQUENCE_TAG_BASE_NAME, create_sequence_custom_coordinate_system_capture_rule(level), level)
        custom_coordinate_captures.extend([base_context, pair_context, sequence_context])
        
    for custom_coordinate_capture in custom_coordinate_captures:
        coordinate_context = custom_coordinate_capture.coordinate_context
        capture_to_override = captures_to_override_by_level[coordinate_context.level]
        @coordinate_context.context.capture("user." + capture_to_override, rule = custom_coordinate_capture.rule)
        def new_capture(m) -> str:
            return compute_coordinates_from_utterance(m)
        module.tag(coordinate_context.tag, desc=f"Tag for the level {coordinate_context.level} of the capture {coordinate_context.input_coordinate_capture_name}")
        override_contexts.append(coordinate_context)

build_override_contexts()

def compute_tag_start_for_category(category: InputCoordinateSystemCategory):
    result = ""
    if category == InputCoordinateSystemCategory.LETTER_PAIR:
        result = "letter_pair"
    elif category == InputCoordinateSystemCategory.NUMBER_SEQUENCE:
        result = "number_sequence"
    elif category == InputCoordinateSystemCategory.SINGLE_NUMBER:
        result = "single_number"
    elif category == InputCoordinateSystemCategory.LOWERCASE_LETTER_PAIR:
        result = "lowercase_letter_pair"
    elif category == InputCoordinateSystemCategory.CUSTOM:
        result = "custom_coordinates"
    elif category == InputCoordinateSystemCategory.CUSTOM_PAIR:
        result = "custom_coordinates_pair"
    elif category == InputCoordinateSystemCategory.CUSTOM_SEQUENCE:
        result = "custom_coordinates_sequence"
    if result:
        result = f"mouse_control_chicken_{result}"
    return result

def compute_tag_for_coordinate_system_category_and_depth(category: InputCoordinateSystemCategory, depth: int) -> str:
    category_tag_start = compute_tag_start_for_category(category)
    if not category_tag_start:
        return None
    return f"user.{category_tag_start}_{depth}"


def compute_category_tags(grid: Grid):
    categories = compute_categories(grid)
    result = []
    for index, category in enumerate(categories):
        tag = compute_tag_for_coordinate_system_category_and_depth(category, index + 1)
        if tag:
            result.append(tag)  
    return result


def compute_level_for_tag(tag: str) -> int:
    last_underscore_index = tag.rfind("_")
    if last_underscore_index == -1:
        return 0
    level_text = tag[last_underscore_index + 1:]
    level = int(level_text)
    return level

def compute_appropriate_level_tag_from_category_tags(category_tags):
    maximum_level = 0
    for tag in category_tags:
        level = compute_level_for_tag(tag)
        if level > maximum_level:
            maximum_level = level
    if maximum_level > 0 and maximum_level < DEPTH_LIMIT + 1:
        return 'user.' + compute_level_tag(maximum_level)
    return None

