from .Grid import Rectangle, FlatRectangularGrid
from .RectangularGrid import ListBasedGrid
from typing import List, Generator
from ..fire_chicken.mouse_position import MousePosition
from ..input_coordinates.InputCoordinateSystem import ListCoordinateSystem

class FlatListBasedGrid(FlatRectangularGrid):
    def __init__(self, dimensions: tuple[int, int], coordinates_list: list[str], custom_coordinate_system_name="", separator: str = " "):
        self.dimensions = dimensions
        size = dimensions[0] * dimensions[1]
        if len(coordinates_list) < size:
            raise ValueError("The number of coordinates is less than the number of positions on the grid")
        self.coordinates_list = coordinates_list[:size]
        vertical_num = dimensions[0]
        horizontal_num = dimensions[1]
        horizontal_coordinates_list = [str(i) for i in range(horizontal_num)]
        vertical_coordinates_list = [str(i) for i in range(vertical_num)]
        self.list_based_grid = ListBasedGrid(
            horizontal_coordinates_list,
            vertical_coordinates_list,
            custom_coordinate_system_name,
            separator
        )
        self.coordinate_system = ListCoordinateSystem(
            self.coordinates_list,
            custom_coordinate_system_name,
            separator
        )
        self.converter = {}
        for v in range(vertical_num):
            for h in range(horizontal_num):
                coordinate_string = f"{v}{separator}{h}"
                target_index = self._compute_index_from_intermediate_coordinates(h, v)
                self.converter[self.coordinates_list[target_index]] = coordinate_string

    def _compute_index_from_intermediate_coordinates(self, horizontal: str, vertical: str) -> int:
        return horizontal + vertical * self.dimensions[1]

    def compute_combined_coordinates(self, intermediate_horizontal: str, intermediate_vertical: str):
        index = self._compute_index_from_intermediate_coordinates(
            int(intermediate_horizontal),
            int(intermediate_vertical)
        )
        return self.coordinates_list[index]

    def _convert_coordinates_to_intermediate_form(self, coordinates: str) -> str:
        return self.converter[coordinates]

    def make_around(self, rectangle: Rectangle) -> None:
        self.list_based_grid.make_around(rectangle)
    
    def compute_sub_rectangle_for(self, grid_coordinates: str) -> Rectangle:
        converted_coordinates = self._convert_coordinates_to_intermediate_form(grid_coordinates)
        return self.list_based_grid.compute_sub_rectangle_for(converted_coordinates)

    def compute_absolute_position_from_valid_coordinates(self, grid_coordinates: str) -> MousePosition:
        converted_coordinates = self._convert_coordinates_to_intermediate_form(grid_coordinates)
        return self.list_based_grid.compute_absolute_position_from_valid_coordinates(converted_coordinates)

    def get_horizontal_coordinates(self) -> Generator:
        for element in self.list_based_grid.get_horizontal_coordinates(): yield element

    def get_vertical_coordinates(self) -> Generator:
        for element in self.list_based_grid.get_vertical_coordinates(): yield element

    def compute_absolute_horizontal_from(self, coordinates: str) -> int:
        converted_coordinates = self._convert_coordinates_to_intermediate_form(coordinates)
        return self.list_based_grid.compute_absolute_horizontal_from(converted_coordinates)
    
    def compute_absolute_vertical_from(self, coordinates: str) -> int:
        converted_coordinates = self._convert_coordinates_to_intermediate_form(coordinates)
        return self.list_based_grid.compute_absolute_vertical_from(converted_coordinates)

    def compute_absolute_horizontal_from_horizontal_coordinates(self, coordinates: str) -> int:
        converted_coordinates = self._convert_coordinates_to_intermediate_form("0" + self.list_based_grid.separator + coordinates)
        return self.list_based_grid.compute_absolute_horizontal_from(converted_coordinates)

    def compute_absolute_vertical_from_from_vertical_coordinates(self, coordinates: str) -> int:
        converted_coordinates = self._convert_coordinates_to_intermediate_form(coordinates + self.list_based_grid.separator + "0")
        return self.list_based_grid.compute_absolute_vertical_from(converted_coordinates)

    def has_nonoverlapping_sub_rectangles(self) -> bool:
        return False
        
    