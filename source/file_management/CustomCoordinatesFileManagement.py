from .FileUtilities import read_two_columns_from_csv_file, compute_file_names_for_extension, CUSTOM_COORDINATES_DIRECTORY
from talon import Module, app
import os

COORDINATE_FILE_EXTENSION = '.csv'

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_compute_coordinate_list_file_names() -> list[str]:
        '''the names of the coordinate list files'''
        return compute_file_names_for_extension(CUSTOM_COORDINATES_DIRECTORY, COORDINATE_FILE_EXTENSION)

    def mouse_control_chicken_compute_coordinate_columns(file_name: str) -> tuple[list[str], list[str]]:
        '''Obtains the columns of the coordinate list file with the given name'''
        path = os.path.join(CUSTOM_COORDINATES_DIRECTORY, file_name + COORDINATE_FILE_EXTENSION)
        if os.path.exists(path):
            columns = read_two_columns_from_csv_file(path)
            return columns
        else:
            app.notify(f'custom coordinate list file {file_name} does not exist')
