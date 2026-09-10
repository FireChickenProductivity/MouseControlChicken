from enum import Enum, auto

from ..input_coordinates.InputCoordinateSystem import InputCoordinateSystem
from .Grid import Grid, Rectangle
from ..fire_chicken.mouse_position import MousePosition

class SecondaryGridType(Enum):
	NEAR_CURSOR = auto()
	RECENT_POSITONS = auto()

class SecondaryGrid(Grid):
	def handle_using_position_with_mouse_command(self, position: MousePosition) -> None:
		pass

class RecentPositionsGrid(SecondaryGrid):
	"""Shows the last n positions used on the grid"""
	def __init__(
		self,
		n: int,
		input_coordinate_system: InputCoordinateSystem, 
		coordinate_to_position_index
	):
		if n < 1:
			raise ValueError(f"A recent position grid must show at least one position, not {n}!")
		self.n = n
		self.coordinate_system = input_coordinate_system
		self.positions = []
		self.coordinate_to_position_index = coordinate_to_position_index
		self.rectangle = Rectangle

	def make_around(self, rectangle: Rectangle) -> None:
		self.rectangle = rectangle

	def compute_absolute_position_from_valid_coordinates(self, grid_coordinates: str) -> MousePosition:
		index = self.coordinate_to_position_index(grid_coordinates)
		if index < len(self.positions) - 1:
			return None
		return self.positions[index]
	
	def handle_using_position_with_mouse_command(self, position: MousePosition) -> None:
		if len(self.positions) >= self.n:
			self.positions.pop(0)
		self.positions.append(position)
