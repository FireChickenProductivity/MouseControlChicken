#This provides functionality for supporting custom coordinate systems beyond defining the captures

from talon import Module, Context, actions
from .DepthCaptures import DEPTH_LIMIT
from .CoordinatesContext import CoordinateContext
from ..grid.Grid import Grid
from .CoordinateSystemTreeCalculations import compute_custom_ordinate_system_names

module = Module()
default_context = Context()

#Define the talon lists for custom coordinate systems.
def compute_custom_coordinate_system_list_name(level: int):
    return f"mouse_control_chicken_custom_coordinate_system_{level}"
for i in range(1, DEPTH_LIMIT + 1):
    module.list(compute_custom_coordinate_system_list_name(i), desc=f"Custom coordinate system for mouse control chicken {i}")

#This allows updating the current implementation of a certain depth custom coordinate system
#To prevent unnecessary updates, the current name of the custom coordinate system is stored
custom_coordinates_map = {}
def update_custom_coordinate_list(level: int, name: str):
    custom_coordinate_list_name = "user." + compute_custom_coordinate_system_list_name(level)
    if custom_coordinate_list_name not in custom_coordinates_map or custom_coordinates_map[custom_coordinate_list_name] != name:
        custom_coordinates_map[custom_coordinate_list_name] = name
        default_context.lists[custom_coordinate_list_name] = actions.user.mouse_control_chicken_build_coordinate_dictionary(name)

class CustomCoordinatesCaptureContext:
    def __init__(self, base_name: str, rule: str, level: int = 1):
        self.coordinate_context = CoordinateContext(base_name, level)
        self.rule = rule
        
def create_base_custom_coordinate_system_capture_rule(level: int):
    return "{user." + compute_custom_coordinate_system_list_name(level) + "}"

def create_pair_custom_coordinate_system_capture_rule(level: int):
    base_rule = create_base_custom_coordinate_system_capture_rule(level)
    return f"{base_rule} {base_rule}"

def create_sequence_custom_coordinate_system_capture_rule(level: int):
    base_rule = create_base_custom_coordinate_system_capture_rule(level)
    return base_rule + "+"

def update_custom_coordinate_system(grid: Grid):
    names = compute_custom_ordinate_system_names(grid)
    for index, name in enumerate(names):
        if name:
            update_custom_coordinate_list(index + 1, name)

@module.action_class
class Actions:
    def mouse_control_chicken_update_custom_coordinate_system(grid: Grid):
        '''Updates the custom coordinate system lists for the given grid'''
        if grid:
            update_custom_coordinate_system(grid)