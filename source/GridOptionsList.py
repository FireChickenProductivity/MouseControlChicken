from talon import Module, fs, actions, Context, app
from .GridOptions import GridOptions

module = Module()
context = Context()

LIST_NAME = "mouse_control_chicken_grid_options"
LIST_NAME_WITH_PREFIX = 'user.' + LIST_NAME
module.list(LIST_NAME, desc = "The options for the mouse control chicken grid")

GRID_OPTIONS_PATH = actions.user.mouse_control_chicken_get_grid_options_file_path()

options: GridOptions = None
def update_options(name, flags):
    global options
    if name != GRID_OPTIONS_PATH: return 
    options = actions.user.mouse_control_chicken_read_grid_options()
    option_list = {option:option for option in options.get_option_names()}
    context.lists[LIST_NAME_WITH_PREFIX] = option_list

fs.watch(GRID_OPTIONS_PATH, update_options)

def on_ready():
    actions.user.mouse_control_chicken_guarantee_data_directory_exists()
    actions.user.mouse_control_chicken_guarantee_grid_options_file_initialized()
    update_options(GRID_OPTIONS_PATH, "")

app.register("ready", on_ready)