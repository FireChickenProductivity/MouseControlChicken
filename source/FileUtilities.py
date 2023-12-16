from talon import Module, actions
import os
from csv import reader, writer

OUTPUT_DIRECTORY = os.path.join(actions.path.talon_user(), 'Mouse Control Chicken Data')
GRID_OPTIONS_PATH = os.path.join(OUTPUT_DIRECTORY, "GridOptions.csv")

module = Module()
@module.action_class
class Actions:
    def mouse_control_chicken_guarantee_data_directory_exists():
        '''Creates the mouse control chicken data directory if it does not exist'''
        if not os.path.exists(OUTPUT_DIRECTORY):
            os.makedirs(OUTPUT_DIRECTORY)
    
    def mouse_control_chicken_guaranteed_grid_options_file_initialized():
        '''If the grid options file does not exist, this initializes it with defaults'''
        if not os.path.exists(GRID_OPTIONS_PATH):
            with open(GRID_OPTIONS_PATH) as file:
                file_writer = writer(file)
                file_writer.writerow(['one to nine', 'Square Recursive Division Grid', 'UniversalPosition', '3'])
                file_writer.writerow(['alphabet', 'Alphabet', 'RectangularGridFrame', ''])

