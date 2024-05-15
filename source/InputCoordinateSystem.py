from typing import Generator, Tuple, List
from itertools import product

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
    
    def get_separator(self) -> str:
        return self.separator

class InfiniteSequenceCoordinateSystem(InputCoordinateSystem):
    def __init__(self, system: InputCoordinateSystem, separator: str = " "):
        self.system = system
        self.separator = separator
    
    def get_primary_coordinates(self) -> Generator:
        return self.system.get_primary_coordinates()
    
    def do_coordinates_belong_to_system(self, coordinates: str) -> bool:
        if not self.do_coordinates_start_belong_to_system(coordinates): return False
        _, tail = self.split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(coordinates)
        return len(tail) == 0
    
    def do_coordinates_start_belong_to_system(self, coordinates: str) -> bool:
        return self.system.do_coordinates_start_belong_to_system(coordinates)
    
    def split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(self, coordinates: str) -> Tuple[str]:
        head = ""
        tail = coordinates
        unfinished: bool = True
        while unfinished:
            subhead, new_tail = self.system.split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(tail)
            if head and subhead: head += self.separator
            head += subhead
            if len(tail) == 0 or new_tail == tail: unfinished = False
            tail = new_tail
        return head, tail

    def get_infinitely_repeated_system(self) -> InputCoordinateSystem:
        return self.system

class DisjointUnionCoordinateSystem(InputCoordinateSystem):
    def __init__(self, systems: List[InputCoordinateSystem], separator: str = " "):
        self.systems = systems
        self.separator = separator
    
    def do_coordinates_belong_to_system(self, coordinates: str) -> bool:
        for system in self.systems:
            if system.do_coordinates_belong_to_system(coordinates): return True
        return False

    def do_coordinates_start_belong_to_system(self, coordinates: str) -> bool:
        for system in self.systems:
            if system.do_coordinates_start_belong_to_system(coordinates): return True
        return False

    def split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(self, coordinates: str) -> Tuple[str]:
        biggest_matching_coordinates = ("", coordinates)
        for system in self.systems:
            if system.do_coordinates_start_belong_to_system(coordinates): 
                head, tail = system.split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(coordinates)
                if len(head) > len(biggest_matching_coordinates[0]): biggest_matching_coordinates = (head, tail)
        return biggest_matching_coordinates
            
    def get_primary_coordinates(self) -> Generator:
        for system in self.systems:
            for coordinate in system.get_primary_coordinates():
                yield coordinate
                
class SequentialCombinationCoordinateSystem(InputCoordinateSystem):
    def __init__(self, systems: List[InputCoordinateSystem], separator: str = " "):
        self.systems = systems
        self.separator = separator
    
    def get_primary_coordinates(self) -> Generator:
        primary_coordinates = [system.get_primary_coordinates() for system in self.systems]
        for result in product(*primary_coordinates):
            yield self.separator.join(result)

    def do_coordinates_belong_to_system(self, coordinates: str) -> bool:
        remaining_coordinates = coordinates
        for index, system in enumerate(self.systems):
            if not system.do_coordinates_start_belong_to_system(remaining_coordinates): return False
            if system.do_coordinates_belong_to_system(remaining_coordinates): return index == len(self.systems) - 1
            remaining_coordinates = system.split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(coordinates)[1]
    
    def do_coordinates_start_belong_to_system(self, coordinates: str) -> bool:
        remaining_coordinates = coordinates
        for system in self.systems:
            if not system.do_coordinates_start_belong_to_system(remaining_coordinates): return False
            remaining_coordinates = system.split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(coordinates)[1]
        return True
    
    def split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(self, coordinates: str) -> Tuple[str]:
        remaining_coordinates = coordinates
        head = ""
        for system in self.systems:
            part_belonging_to_system, remaining_coordinates = system.split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(remaining_coordinates)
            if head and part_belonging_to_system: head += self.separator
            head += part_belonging_to_system
        return head, remaining_coordinates

class SingleCoordinateCoordinateSystem(InputCoordinateSystem):
    def do_coordinates_belong_to_system(self, coordinates: str) -> bool:
        coordinate_list = self.compute_coordinate_list(coordinates)
        return len(coordinate_list) == 1  and self.does_single_coordinate_belong_to_system(coordinate_list[0])

    def do_coordinates_start_belong_to_system(self, coordinates: str) -> bool:
        coordinate_list = self.compute_coordinate_list(coordinates)
        return self.does_single_coordinate_belong_to_system(coordinate_list[0])

    def split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system(self, coordinates: str) -> Tuple[str]:
        if self.do_coordinates_start_belong_to_system(coordinates):
            coordinate_list = self.compute_coordinate_list(coordinates)
            return coordinate_list[0], self.separator.join(coordinate_list[1:])
        return "", coordinates

    def does_single_coordinate_belong_to_system(self, coordinate: str) -> bool:
        pass

class ListCoordinateSystem(SingleCoordinateCoordinateSystem):
    def __init__(self, coordinate_list: List[str], separator: str = " "):
        self.coordinates = set(coordinate_list)
        self.separator = separator
    
    def get_primary_coordinates(self) -> Generator:
        for coordinate in self.coordinates: yield coordinate

    def does_single_coordinate_belong_to_system(self, coordinate: str) -> bool:
        return coordinate in self.coordinates

class SimpleNumericCoordinateSystem(SingleCoordinateCoordinateSystem):
    def __init__(self, minimum: int, maximum: int, separator: str = " "):
        self.minimum = minimum
        self.maximum = maximum
        self.separator = separator
    
    def get_primary_coordinates(self) -> Generator:
        for coordinate in range(self.minimum, self.maximum + 1): yield str(coordinate)
    
    def does_single_coordinate_belong_to_system(self, coordinate: str) -> bool:
        return coordinate.isdigit() and self.number_is_in_range(int(coordinate))

    def number_is_in_range(self, number: int):
        return self.minimum <= number and number <= self.maximum