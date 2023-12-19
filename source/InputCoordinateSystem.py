from typing import Generator, Tuple

class InputCoordinateSystem:
    def get_primary_coordinates() -> Generator:
        pass
    
    def do_coordinates_belong_to_system(coordinates: str) -> bool:
        pass
    
    def do_coordinates_start_belong_to_system(coordinates: str) -> bool:
        pass
    
    def split_coordinates_with_head_belonging_to_system_and_tail_belonging_to_another_system() -> Tuple[str]:
        pass
    
    def get_name() -> str:
        pass

