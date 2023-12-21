from talon import Module, Context

module = Module()
GRID_SHOWING_TAG_NAME = 'mouse_control_chicken_showing'
GRID_SHOWING_TAG = 'user.' + GRID_SHOWING_TAG_NAME
module.tag(GRID_SHOWING_TAG_NAME, desc = 'Tag for enabling mouse controlled chicken commands for working with the active grid')
GRID_OPTIONS_TAG_NAME = 'mouse_control_chicken_grid_options_showing'
GRID_OPTIONS_TAG = 'user.' + GRID_OPTIONS_TAG_NAME
module.tag(GRID_OPTIONS_TAG_NAME, desc = 'Tag for enabling choosing between mouse control chicken grid options')
grid_open_context = Context()
options_display_context = Context()

@module.action_class
class Actions:
    def mouse_control_chicken_enable_grid_showing_tag():
        '''Enables commands for working with the active mouse control chicken grid'''
        assign_tag_to_context(grid_open_context, GRID_SHOWING_TAG)
    
    def mouse_control_chicken_disable_grid_showing_tag():
        '''Disables commands for working with the active mouse control chicken grid'''
        remove_tags_from_context(grid_open_context)

    def mouse_control_chicken_enable_options_display_tag(tag: str):
        '''Enables the specified options display tag'''
        assign_tag_to_context(options_display_context, tag)
    
    def mouse_control_chicken_disable_options_display_tag():
        '''Disables the specified options display tag'''
        remove_tags_from_context(options_display_context)
    
def assign_tag_to_context(context, tag):
    context.tags = [tag]

def remove_tags_from_context(context):
    context.tags = []