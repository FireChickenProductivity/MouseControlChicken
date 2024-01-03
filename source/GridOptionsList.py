from talon import Module, fs, actions, Context, app
from .GridOptions import GridOptions
from .file_management.FileUtilities import *

module = Module()
context = Context()

LIST_NAME = "mouse_control_chicken_grid_option"
LIST_NAME_WITH_PREFIX = 'user.' + LIST_NAME
module.list(LIST_NAME, desc = "The options for the mouse control chicken grid")
@module.capture(rule = f"{{{LIST_NAME_WITH_PREFIX}}}")
def mouse_control_chicken_grid_option(m) -> str:
    return m.mouse_control_chicken_grid_option

GRID_OPTIONS_PATH = None

options: GridOptions = None
def update_options(name, flags):
    global options
    options = read_grid_options()
    option_list = {option:option for option in options.get_option_names()}
    context.lists[LIST_NAME_WITH_PREFIX] = option_list

def guarantee_grid_options_file_initialized():
    '''If the grid options file does not exist, this initializes it with defaults'''
    options = create_default_grid_options()
    grid_options_path = compute_path_within_output_directory("GridOptions.csv")
    guarantee_csv_file_is_initialized(grid_options_path, convert_grid_options_to_rows(options))

def create_grid_option_rows() -> List[List[str]]:
    default_options = create_default_grid_options()
    option_rows = convert_grid_options_to_rows(default_options)
    return option_rows

def create_default_grid_options():
    return GridOptions([
            GridOption('one to nine', 'Square Recursive Division Grid', 'DoubleNarrow', '3'),
            GridOption('alphabet', 'Alphabet', 'RectangularGridFrame', ''),
            GridOption('double alphabet', 'Double Alphabet', 'RectangularGridFrame', ''),
            GridOption('alphabet numbers', 'Recursively Divisible Combination', 'UniversalPosition', 'alphabet:one to nine'),
            GridOption('double alphabet numbers', 'Recursively Divisible Combination', 'UniversalPosition', 'double alphabet:one to nine')
            ])

def convert_grid_options_to_rows(options: GridOptions) -> List[List[str]]:
    option_rows = []
    for name in options.get_option_names():
        option = options.get_option(name)
        option_rows.append([option.get_name(), option.get_factory_name(), option.get_default_display_option(), option.get_argument()])
    return option_rows

def convert_grid_option_to_row(option: GridOption) -> List[List[str]]:
    return [[option.get_name(), option.get_factory_name(), option.get_default_display_option(), option.get_argument()]]

def on_ready():
    global GRID_OPTIONS_PATH
    GRID_OPTIONS_PATH = get_grid_options_file_path()
    guarantee_data_directory_exists()
    guarantee_grid_options_file_initialized()
    fs.watch(GRID_OPTIONS_PATH, update_options)
    update_options(GRID_OPTIONS_PATH, "")

@module.action_class
class Actions:
    def mouse_control_chicken_get_grid_options() -> GridOptions:
        '''Returns the mouse control chicken grid options'''
        global options
        return options

app.register("ready", on_ready)