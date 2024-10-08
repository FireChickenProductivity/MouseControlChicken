from .Grid import Grid, RectangularGrid
from typing import List

class TreeComputationOptions:
    def __init__(self, *, keep_coordinate_system_modifying_wrappers: bool = False):
        self.keep_coordinate_system_modifying_wrappers = keep_coordinate_system_modifying_wrappers

def compute_primary_grid(grid: Grid):
    return compute_sub_grids(grid)[0]

def compute_sub_grids_for_wrapper(grid: Grid):
    result = compute_sub_grids(grid.get_wrapped_grid())
    if grid.supports_reversed_coordinates() and grid.is_doubling():
        result[0] = grid
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
    
    def has_single_child(self):
        return len(self.children) == 1

    def has_multiple_children(self):
        return len(self.children) > 1
    
    def get_children(self):
        return self.children[:]
    
    def has_value(self):
        return self.value is not None
    
    def add_children(self, children):
        self.children.extend(children)

def compute_primary_most_grid(grid: Grid):
    if grid.is_combination():
        return compute_primary_most_grid(grid.get_primary_grid())
    return grid

def compute_ordered_list_of_non_combination_grids(grid: Grid) -> List[Grid]:
    result = []
    if grid.is_combination():
        result = compute_ordered_list_of_non_combination_grids(grid.get_primary_grid()) + compute_ordered_list_of_non_combination_grids(grid.get_secondary_grid())
    else:
        result = [grid]
    return result

def is_simple_grid(grid: Grid) -> bool:
    return not (grid.is_combination() or grid.is_wrapper() or grid.is_doubling())

def compute_grid_tree_for_chain_at_combination_grid(chain: List[Grid], index: int, options: TreeComputationOptions) -> Node:
    chain_head = compute_ordered_list_of_non_combination_grids(chain[index])
    chain_tail = chain[index + 1:]
    result = compute_grid_tree_for_chain_of_non_combination_grids(chain_head + chain_tail, 0, options)
    return result

def compute_grid_tree_for_chain_at_simple_grid(chain: List[Grid], index: int, options: TreeComputationOptions) -> Node:
    grid = chain[index]
    if index == len(chain) - 1:
        result = Node(grid, [])
    else:
        result = Node(grid, [compute_grid_tree_for_chain_of_non_combination_grids(chain, index + 1, options)])
    return result

def compute_grid_tree_for_chain_at_non_doubling_wrapper_grid(chain: List[Grid], index: int, options: TreeComputationOptions) -> Node:
    grid: Grid = chain[index]
    if options.keep_coordinate_system_modifying_wrappers and grid.is_coordinate_system_modifying_wrapper():
        result = Node(grid, [compute_grid_tree_for_chain_of_non_combination_grids(chain, index + 1, options)])
    else:
        chain[index] = grid.get_wrapped_grid()
        result = compute_grid_tree_for_chain_of_non_combination_grids(chain, index, options)
    return result

def compute_grid_tree_for_chain_at_wrapper_grid(chain: List[Grid], index: int, options: TreeComputationOptions) -> Node:
    grid: Grid = chain[index]
    if grid.is_doubling():
        value = grid
        primary_chain = chain[:]
        primary_chain[index] = grid.get_primary_grid()
        secondary_chain = chain[:]
        secondary_chain[index] = grid.get_secondary_grid()
        children = [compute_grid_tree_for_chain_of_non_combination_grids(primary_chain, index, options), compute_grid_tree_for_chain_of_non_combination_grids(secondary_chain, index, options)]
        result = Node(value, children)
    else:
        result = compute_grid_tree_for_chain_at_non_doubling_wrapper_grid(chain, index, options)
    return result

def compute_grid_tree_for_chain_of_non_combination_grids(chain: List[Grid], index, options: TreeComputationOptions) -> Node:
    result = None
    grid = chain[index]
    if is_simple_grid(grid): 
        result = compute_grid_tree_for_chain_at_simple_grid(chain, index, options)
    elif grid.is_wrapper():
        result = compute_grid_tree_for_chain_at_wrapper_grid(chain, index, options)
    elif grid.is_combination():
        result = compute_grid_tree_for_chain_at_combination_grid(chain, index, options)
    return result

def compute_grid_tree(grid: Grid, options: TreeComputationOptions = None) -> Node:
    '''Builds a tree representation of the sub grid structure of the given grid such that grid doubling is represented by a node with two children.'''
    if options is None:
        options = TreeComputationOptions()
    chain = compute_ordered_list_of_non_combination_grids(grid)
    return compute_grid_tree_for_chain_of_non_combination_grids(chain, index=0, options=options)

def apply_function_to_grid_tree_nodes(function, tree: Node):
    function(tree)
    for child in tree.get_children():
        apply_function_to_grid_tree_nodes(function, child)
    
def apply_function_to_grid_tree_nodes_with_depth_based_state(function, tree: Node, state):
    state = function(tree, state)
    for child in tree.get_children():
        apply_function_to_grid_tree_nodes_with_depth_based_state(function, child, state)
     
def find_first_grid_tree_node_matching_function(tree: Node, function):
    if function(tree):
        return tree
    for child in tree.get_children():
        result = find_first_grid_tree_node_matching_function(child, function)
        if result is not None:
            return result
    return None

class GridNotFoundException(Exception):
    pass

def is_rectangular_grid(grid: Grid) -> bool:
    primary_grid = compute_primary_grid(grid)
    return isinstance(primary_grid, RectangularGrid)

def is_square_grid(grid: Grid) -> bool:
    if not is_rectangular_grid(grid):
        return False
    primary_grid = compute_primary_grid(grid)
    horizontal_coordinates = [coordinate for coordinate in primary_grid.get_horizontal_coordinates()]
    vertical_coordinates = [coordinate for coordinate in primary_grid.get_vertical_coordinates()]
    return len(horizontal_coordinates) == len(vertical_coordinates)