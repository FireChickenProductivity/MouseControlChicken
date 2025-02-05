from ..grid.Grid import Grid
from ..grid.GridCalculations import Node, compute_grid_tree, TreeComputationOptions
from ..input_coordinates.InputCoordinateSystem import InputCoordinateSystem

def _compute_properties_from_coordinate_systems(grid: Grid, append_property_to_list):
    result = []
    tree_computation_options = TreeComputationOptions(keep_coordinate_system_modifying_wrappers=True)
    tree = compute_grid_tree(grid, tree_computation_options)
    while tree:
        append_property_to_list(tree, result)
        if tree.has_children():
            tree = tree.get_children()[0]
        else:
            tree = None
    return result

def _append_single_child_tree_node_category_to_list(tree: Node, input_list: list, compute_property):
    number_of_children = len(tree.get_children())
    if number_of_children < 2:
        node_grid = tree.get_value()
        coordinate_system = node_grid.get_coordinate_system()
        node_property = compute_property(coordinate_system)
        input_list.append(node_property)

def _append_tree_node_category_to_list(tree: Node, input_list: list):
    _append_single_child_tree_node_category_to_list(tree, input_list, lambda coordinate_system: coordinate_system.get_category())

def compute_categories(grid: Grid):
    return _compute_properties_from_coordinate_systems(grid, _append_tree_node_category_to_list)

def _append_custom_coordinate_system_name_to_list(tree: Node, input_list: list):
    def compute_name(coordinate_system: InputCoordinateSystem):
        if coordinate_system.is_custom():
            return coordinate_system.get_custom_coordinate_name()
        return ""
    _append_single_child_tree_node_category_to_list(tree, input_list, compute_name)

def compute_custom_ordinate_system_names(grid: Grid):
    return _compute_properties_from_coordinate_systems(grid, _append_custom_coordinate_system_name_to_list)