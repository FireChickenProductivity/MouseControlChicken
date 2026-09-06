from ..grid.SecondaryGrid import *
from ..grid.Grid import Grid
from .Display import Display

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

