def _compute_indexes_to_avoid(number_of_coordinates):
        middle_index = number_of_coordinates // 2 - 1
        coordinates_to_avoid = [middle_index]
        if number_of_coordinates % 2 == 0:
            coordinates_to_avoid.append(middle_index + 1)
        return coordinates_to_avoid

def compute_coordinate_list_half_splits(coordinate_list):
    number_of_coordinates = len(coordinate_list)
    middle_start = number_of_coordinates // 2 - 1
    middle_end = middle_start
    if number_of_coordinates % 2 == 0:
        middle_end += 1
    start = coordinate_list[:middle_start]
    end = coordinate_list[middle_end + 1:]
    return start, end

class InputCoordinatesDiagonal:
    def __init__(self, coordinates, separator, *, generate_alternate_positions: bool = False):
        self.horizontal_coordinates = coordinates[0]
        self.vertical_coordinates = coordinates[1]
        self.separator = separator
        self.generate_alternate_positions = generate_alternate_positions
    
    def get_coordinate_at(self, index: int):
        return self.vertical_coordinates[index] + self.separator + self.horizontal_coordinates[index]
    
    def get_length(self):
        return len(self.vertical_coordinates)
    
    def generate_coordinates(self):
        number_of_coordinates = len(self.vertical_coordinates)
        coordinates_to_avoid = []
        if self.generate_alternate_positions:
            coordinates_to_avoid = _compute_indexes_to_avoid(number_of_coordinates)
        for i in range(number_of_coordinates):
            if i not in coordinates_to_avoid:
                yield self.vertical_coordinates[i] + self.separator + self.horizontal_coordinates[i]
            
    def get_horizontal_coordinates(self):
        return self.horizontal_coordinates[:]
    
    def get_vertical_coordinates(self):
        return self.vertical_coordinates[:]
    
    def get_separator(self):
        return self.separator
    
    def create_reverse_diagonal(self, *, generate_alternate_positions: bool = False):
        horizontal_coordinates = self.horizontal_coordinates[:]
        vertical_coordinates = self.vertical_coordinates[:]
        vertical_coordinates.reverse()
        return InputCoordinatesDiagonal((horizontal_coordinates, vertical_coordinates), self.separator, generate_alternate_positions=generate_alternate_positions)
    
    def create_half_diagonals(self, *, generate_alternate_positions: bool = False):
        left_horizontal, right_horizontal = compute_coordinate_list_half_splits(self.horizontal_coordinates)
        top_vertical, bottom_vertical = compute_coordinate_list_half_splits(self.vertical_coordinates)
        if len(left_horizontal) % 2 == 1:
            coordinate_lists = [left_horizontal, right_horizontal, top_vertical, bottom_vertical]
            half_middle = len(left_horizontal) // 2 - 1
            for coordinate_list in coordinate_lists:
                coordinate_list.pop(half_middle)
        half_diagonals = [
            InputCoordinatesDiagonal((left_horizontal, top_vertical), self.separator, generate_alternate_positions=generate_alternate_positions),
            InputCoordinatesDiagonal((right_horizontal, bottom_vertical), self.separator, generate_alternate_positions=generate_alternate_positions)
        ]
        return half_diagonals
    
    def create_half_reverse_diagonals(self, *, generate_alternate_positions: bool = False):
        half_diagonals = self.create_half_diagonals(generate_alternate_positions=generate_alternate_positions)
        reverse_diagonals = [diagonal.create_reverse_diagonal(generate_alternate_positions=generate_alternate_positions) for diagonal in half_diagonals]
        return reverse_diagonals

class SubDiagonals:
    def __init__(self, division_factor: int ):
        self.division_factor = division_factor
        self.main_diagonals = []
        self.display_diagonals = []
        for diagonals in [self.main_diagonals, self.display_diagonals]:
            diagonals.extend([[] for i in range(division_factor + 1)])
    
    def set_main_diagonals(self, diagonals, index: int):
        self.main_diagonals[index] = diagonals

    def set_display_diagonals(self, diagonals, index: int):
        self.display_diagonals[index] = diagonals
    
    def get_display_diagonals(self, index: int):
        return self.display_diagonals[index]
    
    def get_main_diagonals(self, index: int):
        return self.main_diagonals[index]
    
    def get_diagonals(self, index: int):
        total_display_diagonals = []
        for i in range(index + 1):
            total_display_diagonals.extend(self.display_diagonals[i])
        return total_display_diagonals

class DiagonalComputer:
    def __init__(self, primary_diagonal: InputCoordinatesDiagonal, division_factor: int = 0):
        self.primary_diagonal = primary_diagonal
        self.division_factor = division_factor
        self.diagonals = SubDiagonals(division_factor)
        self.compute_diagonals()

    def compute_diagonals(self):
        self.diagonals.set_main_diagonals([self.primary_diagonal], 0)
        self.diagonals.set_display_diagonals([self.primary_diagonal.create_reverse_diagonal(generate_alternate_positions=True)], 0)
        for i in range(1, self.division_factor + 1):
            previous_diagonals = self.diagonals.get_main_diagonals(i - 1)
            current_diagonals = []
            for diagonal in previous_diagonals:
                current_diagonals.extend(diagonal.create_half_diagonals(generate_alternate_positions=False))
            reverse_diagonals = [diagonal.create_reverse_diagonal(generate_alternate_positions=True) for diagonal in current_diagonals]
            self.diagonals.set_main_diagonals(current_diagonals, i)
            self.diagonals.set_display_diagonals(reverse_diagonals, i)

    def compute_diagonals(self):
        self.diagonals.set_main_diagonals([self.primary_diagonal, self.primary_diagonal.create_reverse_diagonal()], 0)
        self.diagonals.set_display_diagonals([self.primary_diagonal.create_reverse_diagonal(generate_alternate_positions=True), self.primary_diagonal], 0)
        for i in range(1, self.division_factor + 1):
            previous_diagonals = self.diagonals.get_main_diagonals(i - 1)
            new_display_diagonals = []
            for diagonal in previous_diagonals:
                new_display_diagonals.extend(diagonal.create_half_reverse_diagonals(generate_alternate_positions=True))
            self.diagonals.set_display_diagonals(new_display_diagonals, i)
            new_main_diagonals = []
            for diagonal in previous_diagonals:
                new_main_diagonals.extend(diagonal.create_half_diagonals(generate_alternate_positions=False))
                new_main_diagonals.extend(diagonal.create_half_reverse_diagonals(generate_alternate_positions=False))
            self.diagonals.set_main_diagonals(new_main_diagonals, i)
            
    def get_diagonals(self):
        return self.diagonals.get_diagonals(self.division_factor)