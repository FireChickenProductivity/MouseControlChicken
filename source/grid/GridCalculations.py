from .Grid import Grid
from .ReverseCoordinateDoublingGrid import ReverseCoordinateDoublingGrid
from typing import List

def compute_primary_grid(grid: Grid):
    return compute_sub_grids(grid)[0]

def compute_reverse_coordinate_doubling_sub_grid_representation(grid: ReverseCoordinateDoublingGrid):
    primary_grid = compute_primary_grid(grid.get_primary_grid())
    secondary_grid = compute_primary_grid(grid.get_secondary_grid())
    return ReverseCoordinateDoublingGrid(primary_grid, secondary_grid)

def compute_sub_grids_for_wrapper(grid: Grid):
    result = compute_sub_grids(grid.get_wrapped_grid())
    if grid.supports_reversed_coordinates():
        result[0] = compute_reverse_coordinate_doubling_sub_grid_representation(grid)
    return result

def compute_sub_grids(grid: Grid) -> List[Grid]:
    result = []
    if grid.is_combination():
        result = compute_sub_grids(grid.get_primary_grid()) + compute_sub_grids(grid.get_secondary_grid())
    elif grid.is_wrapper():
        result = compute_sub_grids_for_wrapper(grid)
    else:
        result = [grid]
    return result

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def get_value(self):
        return self.value
    
    def has_children(self):
        return len(self.children) > 0
    
    def get_children(self):
        return self.children[:]
    
    def has_value(self):
        return self.value is not None

def compute_grid_tree_for_doubling(grid: ReverseCoordinateDoublingGrid) -> Node:
    value = compute_reverse_coordinate_doubling_sub_grid_representation(grid)
    children = []
    primary_grid_tree = compute_grid_tree(grid.get_primary_grid())
    if primary_grid_tree.has_children():
        secondary_grid_tree = compute_grid_tree(grid.get_secondary_grid())
        # for tree in [primary_grid_tree, secondary_grid_tree]:
        #     children.extend(tree.get_children())
        children = [primary_grid_tree, secondary_grid_tree]
    result = Node(
            value,
            children,
            )
    return result

def compute_grid_tree(grid: Grid) -> Node:
    '''Builds a tree representation of the sub grid structure of the given grid such that grid doubling is represented by a node with two children.'''
    if grid.is_combination():
        result = Node(grid.get_primary_grid(), [compute_grid_tree(grid.get_secondary_grid())])
    elif grid.is_wrapper():
        if grid.supports_reversed_coordinates():
            result = compute_grid_tree_for_doubling(grid)
        else:
            result = compute_grid_tree(grid.get_wrapped_grid())
    else:
        result = Node(grid, [])
    return result

def apply_function_to_grid_tree_nodes(function, tree: Node):
    function(tree)
    for child in tree.get_children():
        apply_function_to_grid_tree_nodes(function, child)
    
def apply_function_to_grid_tree_nodes_with_depth_based_state(function, tree: Node, state):
    state = function(tree, state)
    for child in tree.get_children():
        apply_function_to_grid_tree_nodes_with_depth_based_state(function, child, state)