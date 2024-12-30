from talon import Module, Context
from typing import List
from .grid.Grid import Grid
from .CoordinatesCapture import compute_category_tags, compute_appropriate_level_tag_from_category_tags

module = Module()

GRID_SHOWING_TAG_NAME = 'mouse_control_chicken_showing'
GRID_SHOWING_TAG = 'user.' + GRID_SHOWING_TAG_NAME
module.tag(GRID_SHOWING_TAG_NAME, desc = 'Tag for enabling mouse control chicken commands for working with the active grid')

NARROW_ABLE_GRID_SHOWING_TAG_NAME = 'mouse_control_chicken_narrow_able_showing'
NARROW_ABLE_GRID_SHOWING_TAG = 'user.' + NARROW_ABLE_GRID_SHOWING_TAG_NAME
module.tag(NARROW_ABLE_GRID_SHOWING_TAG_NAME, desc = 'Tag for enabling mouse control chicken commands for working with the active narrow able grid')

REVERSE_COORDINATES_SUPPORTING_GRID_SHOWING_TAG_NAME = 'mouse_control_chicken_reverse_coordinates_supporting_showing'
REVERSE_COORDINATES_SUPPORTING_GRID_SHOWING_TAG = 'user.' + REVERSE_COORDINATES_SUPPORTING_GRID_SHOWING_TAG_NAME
module.tag(REVERSE_COORDINATES_SUPPORTING_GRID_SHOWING_TAG_NAME, desc = 'Tag for enabling mouse control chicken commands for working with a reverse coordinates supporting grid')

GRID_OPTIONS_TAG_NAME = 'mouse_control_chicken_options_showing'
GRID_OPTIONS_TAG = 'user.' + GRID_OPTIONS_TAG_NAME
module.tag(GRID_OPTIONS_TAG_NAME, desc = 'Tag for enabling choosing between mouse control chicken grid options')

GRID_CREATION_TAG_NAME = 'mouse_control_chicken_grid_creation'
GRID_CREATION_TAG = 'user.' + GRID_CREATION_TAG_NAME
module.tag(GRID_CREATION_TAG_NAME, desc = 'Tag for enabling mouse control chicken grid creation commands')

GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG_NAME = 'mouse_control_chicken_grid_creation_argument_two_to_nine'
GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG = 'user.' + GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG_NAME
module.tag(GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG_NAME, desc = 'Tag for setting the current argument type to two to nine for mouse control chicken grid creation')

GRID_CREATION_ARGUMENT_POSITIVE_INTEGER_TAG_NAME = 'mouse_control_chicken_grid_creation_argument_positive_integer'
GRID_CREATION_ARGUMENT_POSITIVE_INTEGER_TAG = 'user.' + GRID_CREATION_ARGUMENT_POSITIVE_INTEGER_TAG_NAME
module.tag(GRID_CREATION_ARGUMENT_POSITIVE_INTEGER_TAG_NAME, desc = 'Tag for setting the current argument type to positive integer for mouse control chicken grid creation')

GRID_CREATION_ARGUMENT_GRID_OPTION_TAG_NAME = 'mouse_control_chicken_grid_creation_argument_grid_option'
GRID_CREATION_ARGUMENT_GRID_OPTION_TAG = 'user.' + GRID_CREATION_ARGUMENT_GRID_OPTION_TAG_NAME
module.tag(GRID_CREATION_ARGUMENT_GRID_OPTION_TAG_NAME, desc = 'Tag for setting the current argument type to grid option for mouse control chicken grid creation')

DICTATION_INPUT_TAG_NAME = 'mouse_control_chicken_dictation_input_showing'
DICTATION_INPUT_TAG = 'user.' + DICTATION_INPUT_TAG_NAME
module.tag(DICTATION_INPUT_TAG_NAME, desc = 'Tag for enabling dictation input for mouse control chicken')

ARGUMENT_INPUT_THROUGH_DICTATION_INPUT_TAG_NAME = 'mouse_control_chicken_argument_input_through_dictation_input'
ARGUMENT_INPUT_THROUGH_DICTATION_INPUT_TAG = 'user.' + ARGUMENT_INPUT_THROUGH_DICTATION_INPUT_TAG_NAME
module.tag(ARGUMENT_INPUT_THROUGH_DICTATION_INPUT_TAG_NAME, desc = 'Tag for enabling argument input through dictation input for mouse control chicken')

DICTATION_INPUT_WITH_OPTIONS_TAG_NAME = 'mouse_control_chicken_dictation_input_with_options'
DICTATION_INPUT_WITH_OPTIONS_TAG = 'user.' + DICTATION_INPUT_WITH_OPTIONS_TAG_NAME
module.tag(DICTATION_INPUT_WITH_OPTIONS_TAG_NAME, desc = 'Tag for enabling dictation input with enumerated options for mouse control chicken')

PAGE_ADJUSTMENT_TAG_NAME = 'mouse_control_chicken_page_adjustment'
PAGE_ADJUSTMENT_TAG = 'user.' + PAGE_ADJUSTMENT_TAG_NAME
module.tag(PAGE_ADJUSTMENT_TAG_NAME, desc = 'Tag for enabling page adjustment commands for mouse control chicken dialogues')

QUICK_ACTION_TAG_NAME = "mouse_control_chicken_quick_action"
QUICK_ACTION_TAG = 'user.' + QUICK_ACTION_TAG_NAME
module.tag(QUICK_ACTION_TAG_NAME, desc="Tag for activating the quick action command which activates an action on dictating the main coordinates for the active mouse control chicken coordinate system")
quick_action_context = Context()

QUICK_DROP_TAG_NAME = "mouse_control_chicken_quick_drop"
QUICK_DROP_TAG = 'user.' + QUICK_DROP_TAG_NAME
module.tag(QUICK_DROP_TAG_NAME, desc="Tag for activating Mouse Control Chicken quick drop")
quick_drop_context = Context()

grid_open_context = Context()
options_dialogue_context = Context()
grid_creation_context = Context()
dictation_input_context = Context()

@module.action_class
class Actions:
    def mouse_control_chicken_enable_grid_showing_tags(grid: Grid):
        '''Enables commands for working with the active mouse control chicken grid'''
        tags = [GRID_SHOWING_TAG]
        if grid.supports_narrowing(): tags.append(NARROW_ABLE_GRID_SHOWING_TAG)
        if grid.supports_reversed_coordinates() or grid.supports_narrowing(): tags.append(REVERSE_COORDINATES_SUPPORTING_GRID_SHOWING_TAG)
        category_tags = compute_category_tags(grid)
        tags.extend(category_tags)
        level_tag_representing__representing_coordinate_system_depth = compute_appropriate_level_tag_from_category_tags(category_tags)
        if level_tag_representing__representing_coordinate_system_depth:
            tags.append(level_tag_representing__representing_coordinate_system_depth)
        assign_tags_to_context(grid_open_context, tags)
    
    def mouse_control_chicken_disable_grid_showing_tags():
        '''Disables commands for working with the active mouse control chicken grid'''
        remove_tags_from_context(grid_open_context)

    def mouse_control_chicken_enable_options_dialogue_tag(tag: str = ""):
        '''Enables the specified options dialogue tag'''
        tags = [GRID_OPTIONS_TAG, PAGE_ADJUSTMENT_TAG]
        if tag: tags.append(tag)
        assign_tags_to_context(options_dialogue_context, tags)
    
    def mouse_control_chicken_disable_options_dialogue_tag():
        '''Disables the specified options dialogue tag'''
        remove_tags_from_context(options_dialogue_context)

    def mouse_control_chicken_enable_grid_creation_tag():
        '''Enables the mouse control chicken grid creation tag'''
        assign_tag_to_context(grid_creation_context, GRID_CREATION_TAG)

    def mouse_control_chicken_disable_grid_creation_tag():
        '''Disables the mouse control chicken grid creation tag'''
        remove_tags_from_context(grid_creation_context)

    def mouse_control_chicken_enable_grid_creation_argument_type_tag(tag: str):
        '''Enables the specified mouse control chicken grid creation argument type tag'''
        assign_tag_to_context(dictation_input_context, tag)
    
    def mouse_control_chicken_disable_grid_creation_argument_type_tag():
        '''Disables the mouse control chicken grid creation argument type tag'''
        remove_tags_from_context(dictation_input_context)

    def mouse_control_chicken_enable_dictation_input_dialogue_tag(secondary_tags: List[str] = []):
        '''Enables the mouse control chicken dictation input dialogue tag and secondary tag'''
        tags = [DICTATION_INPUT_TAG]
        if secondary_tags: tags.extend(secondary_tags)
        assign_tags_to_context(dictation_input_context, tags)
    
    def mouse_control_chicken_disable_dictation_input_dialogue_tag():
        '''Disables the mouse control chicken dictation input dialogue tag'''
        remove_tags_from_context(dictation_input_context)
    
    def mouse_control_chicken_enable_quick_action_context():
        '''Enables the quick action commands'''
        assign_tag_to_context(quick_action_context, QUICK_ACTION_TAG)
    
    def mouse_control_chicken_disable_quick_action_context():
        '''Disables the quick action commands'''
        remove_tags_from_context(quick_action_context)

    def mouse_control_chicken_enable_quick_drop_context():
        '''Enables the quick drop command'''
        assign_tag_to_context(quick_drop_context, QUICK_DROP_TAG)
    
    def mouse_control_chicken_disable_quick_drop_context():
        '''Disables the quick drop command'''
        remove_tags_from_context(quick_drop_context)
    
def assign_tag_to_context(context, tag):
    context.tags = [tag]

def assign_tags_to_context(context, tags):
    context.tags = tags

def remove_tags_from_context(context):
    context.tags = []

  