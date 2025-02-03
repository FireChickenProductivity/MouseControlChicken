from .FileUtilities import read_two_columns_from_csv_file, compute_file_names_for_extension, get_custom_coordinates_directory, build_dictionary_from_two_columns_csv_file
from talon import Module, app
import os

COORDINATE_FILE_EXTENSION = '.csv'

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_compute_coordinate_list_file_names() -> list[str]:
        '''the names of the coordinate list files'''
        return compute_file_names_for_extension(get_custom_coordinates_directory(), COORDINATE_FILE_EXTENSION)

    def mouse_control_chicken_coordinate_list_file_exists(file_name: str) -> bool:
        '''Determines if the coordinate list file with the given name exists'''
        path = os.path.join(get_custom_coordinates_directory(), file_name + COORDINATE_FILE_EXTENSION)
        return os.path.exists(path)

    def mouse_control_chicken_compute_coordinate_columns(file_name: str) -> tuple[list[str], list[str]]:
        '''Obtains the columns of the coordinate list file with the given name'''
        path = create_file_path(file_name)
        if os.path.exists(path):
            columns = read_two_columns_from_csv_file(path)
            return columns
        else:
            notify_user_that_file_does_not_exist(file_name)
            
    def mouse_control_chicken_build_coordinate_dictionary(file_name: str) -> dict[str, str]:
        '''Obtains the dictionary from the coordinate list file with the given name'''
        path = create_file_path(file_name)
        if os.path.exists(path):
            return build_dictionary_from_two_columns_csv_file(path)
        else:
            notify_user_that_file_does_not_exist(file_name)

def create_file_path(file_name: str) -> str:
    return os.path.join(get_custom_coordinates_directory(), file_name + COORDINATE_FILE_EXTENSION)

def notify_user_that_file_does_not_exist(file_name: str):
    app.notify(f'custom coordinate list file {file_name} does not exist')