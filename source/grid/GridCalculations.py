from .Grid import Grid
from .ReverseCoordinateDoublingGrid import ReverseCoordinateDoublingGrid
from typing import List

def compute_primary_grid(grid: Grid):
    return compute_sub_grids(grid)[0]

def compute_sub_grids_for_wrapper(grid: Grid):
    result = compute_sub_grids(grid.get_wrapped_grid())
    if grid.supports_reversed_coordinates():
        primary_grid_for_primary_grid = compute_primary_grid(grid.get_primary_grid())
        primary_grid_for_secondary_grid = compute_primary_grid(grid.get_secondary_grid())
        result[0] = ReverseCoordinateDoublingGrid(primary_grid_for_primary_grid, primary_grid_for_secondary_grid)
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