from ..grid.SecondaryGrid import *
from ..grid.Grid import Grid, get_innermost_combination, has_non_wrapping_combination, obtain_relevant_sub_rectangle_from_grid_at
from .Display import Display
from .Canvas import Canvas, Line

class SecondaryDisplay:
	def __init__(self):
		self.grid: Grid | None = None

	def get_secondary_grid_type(self) -> SecondaryGridType | None:
		"""Returns the type of the secondary grid this is for. Returns None if it is actually for the main grid"""
		return None

	def set_grid(self, grid: Grid): 
		self.grid = grid

	@staticmethod
	def supports_grid(grid: Grid) -> bool:
		return True

	def draw_on(self, canvas: Canvas):
		pass

class SubRectangleDisplay(SecondaryDisplay):
	def __init__(self):
		super().__init__()

	@staticmethod
	def supports_grid(grid: Grid) -> bool:
		return grid.is_combination() and has_non_wrapping_combination(grid)

	def draw_on(self, canvas: Canvas):
		# find the sub grid
		# get its rectangle
		if self.grid is None:
			return 
		relevant_grid = get_innermost_combination(self.grid)
		persistent_coordinates = relevant_grid.get_persistent_coordinates()
		if not persistent_coordinates:
			return 
		are_coordinates_reversed = False # figure this out
		sub_rectangle = obtain_relevant_sub_rectangle_from_grid_at(relevant_grid, persistent_coordinates, are_coordinates_reversed)
		if not sub_rectangle:
			return 
		# draw the rectangle on the canvas using lines
		left = sub_rectangle.left
		right = sub_rectangle.right
		bottom = sub_rectangle.bottom
		top = sub_rectangle.top
		canvas.insert_line(Line(left, top, left, bottom))
		canvas.insert_line(Line(left, bottom, right, bottom))
		canvas.insert_line(Line(right, top, right, bottom))
		canvas.insert_line(Line(left, top, right, top))