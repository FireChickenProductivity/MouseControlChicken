from talon import actions, app
import os
from csv import reader, writer
from typing import List

OUTPUT_DIRECTORY = None
def guarantee_data_directory_exists():
    '''Creates the mouse control chicken data directory if it does not exist'''
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

def initialize():
    global OUTPUT_DIRECTORY
    OUTPUT_DIRECTORY = compute_output_directory()
    guarantee_data_directory_exists()

def compute_output_directory():
    return os.path.join(actions.path.talon_user(), 'Mouse Control Chicken Data')

app.register('ready', initialize)

def compute_path_within_output_directory(file_name: str):
    return os.path.join(OUTPUT_DIRECTORY, file_name)

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

def append_row_to_csv_file(path: str, row: List[str]):
    '''Appends the given row to the csv file at the given path'''
    with open(path, "a", newline = '') as file:
        file_writer = writer(file)
        file_writer.writerow(row)

def read_rows_from_csv_file(path: str) -> List[List[str]]:
    '''Obtains the rows from the csv file at the given path'''
    rows = []
    with open(path, "r", newline = '') as file:
        file_reader = reader(file)
        for row in file_reader:
            if len(row) > 0:
                rows.append(row)
    return rows

def write_text_to_file_if_uninitialized(path: str, text: str):
    guarantee_data_directory_exists()
    '''Writes the given text to the file at the given path if the file does not exist'''
    if not os.path.exists(path):
        with open(path, "w") as file:
            file.write(text)
    


