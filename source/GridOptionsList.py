from talon import Module, fs, Context, app
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
    options = read_grid_options_from_path(GRID_OPTIONS_PATH)
    option_list = {option:option for option in options.get_option_names()}
    context.lists[LIST_NAME_WITH_PREFIX] = option_list

def guarantee_grid_options_file_initialized_at_path(path: str):
    '''If the grid options file does not exist, this initializes it with defaults'''
    options = create_default_grid_options()
    guarantee_csv_file_is_initialized(path, convert_grid_options_to_rows(options))

def write_grid_option(option: GridOption):
    '''Stores the mouse control chicken grid option in the file'''
    row = convert_grid_option_to_row(option)
    append_row_to_csv_file(GRID_OPTIONS_PATH, row)

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

def read_grid_options_from_path(path: str) -> GridOptions:
    '''Obtains the mouse control chicken grid options from the file'''
    options = []
    rows = read_rows_from_csv_file(path)
    for entry in rows:
        if len(entry) == 4:
            option = GridOption(*entry)
            options.append(option)
    return GridOptions(options)
    
def update_option_default_display(option_name: str, display_name: str):
    '''Updates the default display option for the given grid option'''
    options = read_grid_options_from_path(GRID_OPTIONS_PATH)
    option = options.get_option(option_name)
    new_option = GridOption(option.get_name(), option.get_factory_name(), display_name, option.get_argument())
    new_options = [new_option if option_name == new_option.get_name() else options.get_option(option_name) for option_name in options.get_option_names()]
    write_grid_options_file(GridOptions(new_options))

def on_ready():
    global GRID_OPTIONS_PATH
    GRID_OPTIONS_PATH = compute_path_within_output_directory("GridOptions.csv")
    guarantee_data_directory_exists()
    guarantee_grid_options_file_initialized_at_path(GRID_OPTIONS_PATH)
    fs.watch(GRID_OPTIONS_PATH, update_options)
    update_options(GRID_OPTIONS_PATH, "")

@module.action_class
class Actions:
    def mouse_control_chicken_get_grid_options() -> GridOptions:
        '''Returns the mouse control chicken grid options'''
        global options
        return options

app.register("ready", on_ready)