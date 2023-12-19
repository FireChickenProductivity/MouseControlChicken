from typing import Generator, Tuple, List

class InputCoordinateSystem:
    def get_primary_coordinates(self) -> Generator:
        pass
    
    def do_coordinates_belong_to_system(self, coordinates: str) -> bool:
        pass
    
    def do_coordinates_start_belong_to_system(self, coordinates: str) -> bool:
        pass
    
    def split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(self, coordinates: str) -> Tuple[str]:
        pass
    
    def compute_coordinate_list(self, coordinates: str) -> List[str]:
        coordinate_list = coordinates.split(self.separator)
        return coordinate_list

class SequentialCombinationCoordinateSystem:
    def __init__(self, systems: List[InputCoordinateSystem], separator: str = " "):
        self.systems = systems
        self.separator = separator
    
    def do_coordinates_belong_to_system(self, coordinates: str) -> bool:
        remaining_coordinates = coordinates
        for index, system in enumerate(self.systems):
            if not system.do_coordinates_start_belong_to_system(remaining_coordinates): return False
            if system.do_coordinates_belong_to_system(remaining_coordinates): return index == len(self.systems) - 1
            remaining_coordinates = system.split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(coordinates)[1]
    
    def do_coordinates_start_belong_to_system(self, coordinates: str) -> bool:
        remaining_coordinates = coordinates
        for index, system in enumerate(self.systems):
            if not system.do_coordinates_start_belong_to_system(remaining_coordinates): return False
            remaining_coordinates = system.split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(coordinates)[1]
        return True
    
    def split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(self, coordinates: str) -> Tuple[str]:
        remaining_coordinates = coordinates
        head = ""
        for index, system in enumerate(self.systems):
            part_belonging_to_system, remaining_coordinates = system.split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(coordinates)[1]
            if head: head += self.separator
            head += part_belonging_to_system
        return part_belonging_to_system, remaining_coordinates


class SingleCoordinateCoordinateSystem(InputCoordinateSystem):
    def do_coordinates_belong_to_system(self, coordinates: str) -> bool:
        coordinate_list = self.compute_coordinate_list(coordinates)
        return len(coordinate_list) == 1  and self.does_single_coordinate_belong_to_system(coordinate_list[0])

    def do_coordinates_start_belong_to_system(self, coordinates: str) -> bool:
        coordinate_list = self.compute_coordinate_list(coordinates)
        return self.does_single_coordinate_belong_to_system(coordinate_list[0])

    def split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(self, coordinates: str) -> Tuple[str]:
        coordinate_list = self.compute_coordinate_list(coordinates)
        return (coordinate_list[0], self.separator.join(coordinate_list[1:]))

    def does_single_coordinate_belong_to_system(self, coordinate: str) -> bool:
        pass

class ListCoordinateSystem(InputCoordinateSystem):
    def __init__(self, coordinate_list: List[str], separator: str = " "):
        self.coordinates = set(coordinate_list)
        self.separator = separator
    
    def get_primary_coordinates(self) -> Generator:
        for coordinate in self.coordinates: yield coordinate

    def does_single_coordinate_belong_to_system(self, coordinate: str) -> bool:
        return coordinate in self.coordinates

class SimpleNumericCoordinateSystem(InputCoordinateSystem):
    def __init__(self, minimum: int, maximum: int, separator: str = " "):
        self.minimum = minimum
        self.maximum = maximum
        self.separator = separator
    
    def get_primary_coordinates(self) -> Generator:
        for coordinate in range(self.minimum, self.maximum): yield str(coordinate)
    
    def does_single_coordinate_belong_to_system(self, coordinate: str) -> bool:
        return coordinate.isdigit() and self.number_is_in_range(int(coordinate))

    def number_is_in_range(self, number: int):
        return self.minimum <= number and number <= self.maximum




