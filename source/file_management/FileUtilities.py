from ..GridOptions import GridOptions, GridOption
from talon import actions, app
import os
from csv import reader, writer
from typing import List

OUTPUT_DIRECTORY = None
GRID_OPTIONS_PATH = None
creation_registration_stack = []
def initialize():
    global OUTPUT_DIRECTORY, GRID_OPTIONS_PATH
    OUTPUT_DIRECTORY = compute_output_directory()
    GRID_OPTIONS_PATH = os.path.join(OUTPUT_DIRECTORY, "GridOptions.csv")
    global creation_registration_stack

def compute_output_directory():
    return os.path.join(actions.path.talon_user(), 'Mouse Control Chicken Data')

def compute_path_within_output_directory(file_name: str):
    return os.path.join(OUTPUT_DIRECTORY, file_name)

app.register('ready', initialize)

def guarantee_data_directory_exists():
    '''Creates the mouse control chicken data directory if it does not exist'''
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

def write_grid_options_file(options: GridOptions):
    '''Stores the mouse control chicken grid options in the file'''
    option_rows = []
    for name in options.get_option_names():
        option = options.get_option(name)
        option_rows.append([option.get_name(), option.get_factory_name(), option.get_default_display_option(), option.get_argument()])
    write_csv_file(GRID_OPTIONS_PATH, option_rows)

def guarantee_csv_file_is_initialized(path: str, rows: List[List[str]]):
    '''If the csv file does not exist, this initializes it with the given rows'''
    if not os.path.exists(path):
        write_csv_file(path, rows)

def write_csv_file(path: str, rows: List[List[str]]):
    '''Writes the given rows to the csv file at the given path'''
    with open(path, "w", newline = '') as file:
        file_writer = writer(file)
        for row in rows:
            file_writer.writerow(row)

def write_text_to_file_if_uninitialized(path: str, text: str):
    '''Writes the given text to the file at the given path if the file does not exist'''
    if not os.path.exists(path):
        with open(path, "w") as file:
            file.write(text)

def read_grid_options() -> GridOptions:
    '''Obtains the mouse control chicken grid options from the file'''
    options = []
    with open(GRID_OPTIONS_PATH, "r", newline = '') as file:
        file_reader = reader(file)
        for entry in file_reader:
            if len(entry) == 4:
                option = GridOption(*entry)
                options.append(option)
    return GridOptions(options)
    
def update_option_default_display(option_name: str, display_name: str):
    '''Updates the default display option for the given grid option'''
    options = read_grid_options()
    option = options.get_option(option_name)
    new_option = GridOption(option.get_name(), option.get_factory_name(), display_name, option.get_argument())
    new_options = [new_option if option_name == new_option.get_name() else options.get_option(option_name) for option_name in options.get_option_names()]
    write_grid_options_file(GridOptions(new_options))

def write_grid_option(option: GridOption):
    '''Stores the mouse control chicken grid option in the file'''
    with open(GRID_OPTIONS_PATH, "a") as file:
        file_writer = writer(file)
        file_writer.writerow([option.get_name(), option.get_factory_name(), option.get_default_display_option(), option.get_argument()])
    
def get_grid_options_file_path() -> str:
    '''Returns the path to the mouse control chicken grid options file'''
    return GRID_OPTIONS_PATH

