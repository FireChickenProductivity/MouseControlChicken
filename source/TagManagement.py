from talon import Module, Context
from typing import List
from .Grid import Grid

module = Module()

GRID_SHOWING_TAG_NAME = 'mouse_control_chicken_showing'
GRID_SHOWING_TAG = 'user.' + GRID_SHOWING_TAG_NAME
module.tag(GRID_SHOWING_TAG_NAME, desc = 'Tag for enabling mouse control chicken commands for working with the active grid')

NARROW_ABLE_GRID_SHOWING_TAG_NAME = 'mouse_control_chicken_narrow_able_showing'
NARROW_ABLE_GRID_SHOWING_TAG = 'user.' + NARROW_ABLE_GRID_SHOWING_TAG_NAME
module.tag(NARROW_ABLE_GRID_SHOWING_TAG_NAME, desc = 'Tag for enabling mouse control chicken commands for working with the active narrow able grid')

GRID_OPTIONS_TAG_NAME = 'mouse_control_chicken_options_showing'
GRID_OPTIONS_TAG = 'user.' + GRID_OPTIONS_TAG_NAME
module.tag(GRID_OPTIONS_TAG_NAME, desc = 'Tag for enabling choosing between mouse control chicken grid options')

GRID_CREATION_TAG_NAME = 'mouse_control_chicken_grid_creation'
GRID_CREATION_TAG = 'user.' + GRID_CREATION_TAG_NAME
module.tag(GRID_CREATION_TAG_NAME, desc = 'Tag for enabling mouse control chicken grid creation commands')

GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG_NAME = 'mouse_control_chicken_grid_creation_argument_two_to_nine'
GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG = 'user.' + GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG_NAME
module.tag(GRID_CREATION_ARGUMENT_TWO_TO_NINE_TAG_NAME, desc = 'Tag for setting the current argument type to two to nine for mouse control chicken grid creation')

GRID_CREATION_ARGUMENT_GRID_OPTION_TAG_NAME = 'mouse_control_chicken_grid_creation_argument_grid_option'
GRID_CREATION_ARGUMENT_GRID_OPTION_TAG = 'user.' + GRID_CREATION_ARGUMENT_GRID_OPTION_TAG_NAME
module.tag(GRID_CREATION_ARGUMENT_GRID_OPTION_TAG_NAME, desc = 'Tag for setting the current argument type to grid option for mouse control chicken grid creation')

DICTATION_INPUT_TAG_NAME = 'mouse_control_chicken_dictation_input_showing'
DICTATION_INPUT_TAG = 'user.' + DICTATION_INPUT_TAG_NAME
module.tag(DICTATION_INPUT_TAG_NAME, desc = 'Tag for enabling dictation input for mouse control chicken')

ARGUMENT_INPUT_THROUGH_DICTATION_INPUT_TAG_NAME = 'mouse_control_chicken_argument_input_through_dictation_input'
ARGUMENT_INPUT_THROUGH_DICTATION_INPUT_TAG = 'user.' + ARGUMENT_INPUT_THROUGH_DICTATION_INPUT_TAG_NAME
module.tag(ARGUMENT_INPUT_THROUGH_DICTATION_INPUT_TAG_NAME, desc = 'Tag for enabling argument input through dictation input for mouse control chicken')

grid_open_context = Context()
options_display_context = Context()
grid_creation_context = Context()
grid_creation_argument_type_context = Context()

@module.action_class
class Actions:
    def mouse_control_chicken_enable_grid_showing_tags(grid: Grid):
        '''Enables commands for working with the active mouse control chicken grid'''
        tags = [GRID_SHOWING_TAG]
        if grid.supports_narrowing(): tags.append(NARROW_ABLE_GRID_SHOWING_TAG)
        assign_tags_to_context(grid_open_context, tags)
    
    def mouse_control_chicken_disable_grid_showing_tags():
        '''Disables commands for working with the active mouse control chicken grid'''
        remove_tags_from_context(grid_open_context)

    def mouse_control_chicken_enable_options_display_tag(tag: str = ""):
        '''Enables the specified options display tag'''
        tags = [GRID_OPTIONS_TAG]
        if tag: tags.append(tag)
        assign_tags_to_context(options_display_context, tags)
    
    def mouse_control_chicken_disable_options_display_tag():
        '''Disables the specified options display tag'''
        remove_tags_from_context(options_display_context)

    def mouse_control_chicken_enable_grid_creation_tag():
        '''Enables the mouse control chicken grid creation tag'''
        assign_tag_to_context(grid_creation_context, GRID_CREATION_TAG)

    def mouse_control_chicken_disable_grid_creation_tag():
        '''Disables the mouse control chicken grid creation tag'''
        remove_tags_from_context(grid_creation_context)

    def mouse_control_chicken_enable_grid_creation_argument_type_tag(tag: str):
        '''Enables the specified mouse control chicken grid creation argument type tag'''
        assign_tag_to_context(grid_creation_argument_type_context, tag)
    
    def mouse_control_chicken_disable_grid_creation_argument_type_tag():
        '''Disables the mouse control chicken grid creation argument type tag'''
        remove_tags_from_context(grid_creation_argument_type_context)

    def mouse_control_chicken_enable_dictation_input_display_tag(secondary_tags: List[str] = []):
        '''Enables the mouse control chicken dictation input display tag and secondary tag'''
        tags = [DICTATION_INPUT_TAG]
        if secondary_tags: tags.extend(secondary_tags)
        assign_tags_to_context(grid_creation_argument_type_context, tags)
    
    def mouse_control_chicken_disable_dictation_input_display_tag():
        '''Disables the mouse control chicken dictation input display tag'''
        remove_tags_from_context(grid_creation_argument_type_context)
    
def assign_tag_to_context(context, tag):
    context.tags = [tag]

def assign_tags_to_context(context, tags):
    context.tags = tags

def remove_tags_from_context(context):
    context.tags = []