from .GridOptions import GridOptions, GridOption
from talon import Module, actions, app
import os
from csv import reader, writer

OUTPUT_DIRECTORY = None
GRID_OPTIONS_PATH = None
def initialize_paths():
    global OUTPUT_DIRECTORY, GRID_OPTIONS_PATH
    OUTPUT_DIRECTORY = os.path.join(actions.path.talon_user(), 'Mouse Control Chicken Data')
    GRID_OPTIONS_PATH = os.path.join(OUTPUT_DIRECTORY, "GridOptions.csv")

app.register('ready', initialize_paths)

def mouse_control_chicken_guarantee_data_directory_exists():
    '''Creates the mouse control chicken data directory if it does not exist'''
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    
def mouse_control_chicken_guarantee_grid_options_file_initialized():
    '''If the grid options file does not exist, this initializes it with defaults'''
    if not os.path.exists(GRID_OPTIONS_PATH):
        with open(GRID_OPTIONS_PATH, "w", newline = '') as file:
            file_writer = writer(file)
            file_writer.writerow(['one to nine', 'Square Recursive Division Grid', 'UniversalPosition', '3'])
            file_writer.writerow(['alphabet', 'Alphabet', 'RectangularGridFrame', ''])
            file_writer.writerow(['alphabet numbers', 'Recursively Divisible Combination', 'UniversalPosition', 'alphabet:one to nine'])

def mouse_control_chicken_read_grid_options() -> GridOptions:
    '''Obtains the mouse control chicken grid options from the file'''
    options = []
    with open(GRID_OPTIONS_PATH, "r", newline = '') as file:
        file_reader = reader(file)
        for entry in file_reader:
            if len(entry) == 4:
                option = GridOption(*entry)
                options.append(option)
    return GridOptions(options)
    
def mouse_control_chicken_write_grid_option(option: GridOption):
    '''Stores the mouse control chicken grid option in the file'''
    with open(GRID_OPTIONS_PATH) as file:
        file_writer = writer(file)
        file_writer.writerow([option.get_name(), option.get_factory_name(), option.get_default_display_option(), option.get_argument()])
    
def mouse_control_chicken_get_grid_options_file_path() -> str:
    '''Returns the path to the mouse control chicken grid options file'''
    return GRID_OPTIONS_PATH
