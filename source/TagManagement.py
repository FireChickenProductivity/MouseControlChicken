from talon import Module, Context

module = Module()
GRID_SHOWING_TAG_NAME = 'mouse_control_chicken_showing'
GRID_SHOWING_TAG = 'user.' + GRID_SHOWING_TAG_NAME
module.tag(GRID_SHOWING_TAG_NAME, desc = 'Tag for enabling mouse controlled chicken commands for working with the active grid')
grid_open_context = Context()

@module.action_class
class Actions:
    def mouse_control_chicken_enable_grid_showing_tag():
        '''Enables commands for working with the active mouse control chicken grid'''
        assign_tag_to_context(grid_open_context, GRID_SHOWING_TAG)
    
    def mouse_control_chicken_disable_grid_showing_tag():
        '''Disables commands for working with the active mouse control chicken grid'''
        remove_tags_from_context(grid_open_context)
    
def assign_tag_to_context(context, tag):
    context.tags = [tag]

def remove_tags_from_context(context):
    context.tags = []