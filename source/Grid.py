from .fire_chicken.mouse_position import MousePosition
from typing import Generator, List
from .InputCoordinateSystem import InputCoordinateSystem, ListCoordinateSystem, SequentialCombinationCoordinateSystem, InfiniteSequenceCoordinateSystem, DisjointUnionCoordinateSystem

class Rectangle:
    '''Rectangle holds the coordinates of the sides of a rectangle'''
    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

class CoordinatesNotSupportedException(Exception): pass

class Grid:
    '''Grid is responsible for mapping from a grid coordinate system to absolute coordinates within a given rectangle on the screen'''
    def make_around(self, rectangle: Rectangle) -> None: pass

    def compute_absolute_position_from(self, grid_coordinates: str) -> MousePosition: 
        if self.coordinate_system.do_coordinates_belong_to_system(grid_coordinates):
            return self.compute_absolute_position_from_valid_coordinates(grid_coordinates)
        raise CoordinatesNotSupportedException()

    def compute_absolute_position_from_valid_coordinates(self, grid_coordinates: str) -> MousePosition: pass

    def get_coordinate_system(self) -> InputCoordinateSystem:
        return self.coordinate_system

    def _compute_coordinates(self, grid_coordinates: str) -> List:
        if len(self.separator) == 0: 
            return grid_coordinates
        else:
            return grid_coordinates.split(self.separator)

class VerticallyOrderedGrid(Grid):
    '''VerticallyOrderedGrid is responsible for handling a vertically ordered coordinate system'''
    def get_vertical_coordinates(self) -> Generator: pass
    def compute_absolute_vertical_from(self, coordinates: str) -> int: pass
    def compute_absolute_vertical_from_from_vertical_coordinates(self, coordinates: str) -> int: pass

class HorizontallyOrderedGrid(Grid):
    '''HorizontallyOrderedGrid is responsible for handling a horizontally ordered coordinate system'''
    def get_horizontal_coordinates(self) -> Generator: pass
    def compute_absolute_horizontal_from(self, coordinates: str) -> int: pass
    def compute_absolute_horizontal_from_horizontal_coordinates(self, coordinates: str) -> int: pass

class RecursivelyDivisibleGrid(Grid):
    def compute_sub_rectangle_for(self, grid_coordinates: str) -> Rectangle: pass

class RecursiveDivisionGrid(RecursivelyDivisibleGrid):
    '''RecursiveDivisionGrid offers a coordinate system that recursively divides a given rectangle into smaller regions such that the center of
        the region formed by a series of recursive divisions is the absolute position given by the series of coordinates causing that division'''
    def narrow_grid_using_coordinates(self, grid_coordinates: str) -> None: 
        if self.coordinate_system.do_coordinates_belong_to_system(grid_coordinates):
            return self.narrow_grid_using_valid_coordinates(grid_coordinates)
        raise CoordinatesNotSupportedException()
        
    def narrow_grid_using_valid_coordinates(self, grid_coordinates: str) -> None: pass
    def compute_current_position(self) -> MousePosition: pass
    def reset_grid(self) -> None: pass
    def get_regions(self) -> Generator: pass
    def get_narrowing_options(self) -> Generator: pass

    def build_coordinate_system(self):
        options = [option for option in self.get_narrowing_options()]
        base_system = ListCoordinateSystem(options)
        self.coordinate_system = InfiniteSequenceCoordinateSystem(base_system)

class RectangularGrid(RecursivelyDivisibleGrid, VerticallyOrderedGrid, HorizontallyOrderedGrid):
    '''RectangularGrid offers a coordinate system that divides the given rectangle into a rectangular coordinate system such that
        the positions are determined by a vertical and a horizontal axis'''
    def get_coordinate_pairs(self) -> Generator:
        for horizontal in self.get_horizontal_coordinates():
            for vertical in self.get_vertical_coordinates():
                yield vertical + self.separator + horizontal
    
    def build_coordinate_system(self):
        horizontal_coordinates = [horizontal for horizontal in self.get_horizontal_coordinates()]
        vertical_coordinates = [vertical for vertical in self.get_vertical_coordinates()]
        horizontal_system = ListCoordinateSystem(horizontal_coordinates)
        vertical_system = ListCoordinateSystem(vertical_coordinates)
        self.coordinate_system = SequentialCombinationCoordinateSystem([vertical_system, horizontal_system])

class RecursivelyDivisibleGridCombination(RecursivelyDivisibleGrid):
    def __init__(self, primary: RecursivelyDivisibleGrid, secondary: RecursivelyDivisibleGrid):
        self.primary = primary
        self.secondary = secondary
        self.primary_coordinate_system = primary.get_coordinate_system()
        self.secondary_coordinate_system = secondary.get_coordinate_system()
        self.coordinate_system = DisjointUnionCoordinateSystem([
            self.primary_coordinate_system,
            SequentialCombinationCoordinateSystem([
                self.primary_coordinate_system,
                self.secondary_coordinate_system
            ])
        ])
    
    def get_coordinate_system(self) -> InputCoordinateSystem:
        return self.primary_coordinate_system
    
    def get_secondary_coordinate_system(self) -> InputCoordinateSystem:
        return self.secondary_coordinate_system
    
    def compute_absolute_position_from_valid_coordinates(self, grid_coordinates: str) -> MousePosition:
        print('?????????', f'{{{grid_coordinates}}}')
        head, tail = self.primary_coordinate_system.split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(grid_coordinates)
        print('???????', f'{{{head}}}', ",", f'{{{tail}}}')
        if tail:
            rectangle = self.primary.compute_sub_rectangle_for(head)
            print('rectangle', rectangle)
            self.secondary.make_around(rectangle)
            position = self.secondary.compute_absolute_position_from_valid_coordinates(tail)
        else:
            position = self.primary.compute_absolute_position_from_valid_coordinates(head)
        return position

    def make_around(self, rectangle: Rectangle) -> None:
        self.primary.make_around(rectangle)

    def compute_sub_rectangle_for(self, grid_coordinates: str) -> Rectangle:
        head, tail = self.primary_coordinate_system.split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(grid_coordinates)
        primary_sub_rectangle = self.primary.compute_sub_rectangle_for(head)
        self.secondary.make_around(primary_sub_rectangle)
        rectangle = self.secondary.compute_sub_rectangle_for(tail)
        return rectangle
        
