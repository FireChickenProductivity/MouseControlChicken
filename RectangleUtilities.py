from .Grid import Rectangle
from .fire_chicken.mouse_position import MousePosition

def compute_center_position(rectangle: Rectangle) -> MousePosition:
    horizontal = compute_average(rectangle.left, rectangle.right)
    vertical = compute_average(rectangle.top, rectangle.bottom)
    center = MousePosition(int(horizontal), int(vertical))
    return center

def compute_sub_rectangle(rectangle: Rectangle, number_of_horizontal_divisors: int, number_of_vertical_divisors: int, horizontal: int, vertical: int):
    pass

def compute_line_divisors(start_amount: int, ending_amount: int, number_of_divisors: int):
    if start_amount == ending_amount: return [start_amount]
    division_size = int((ending_amount - start_amount)/(number_of_divisors + 1))
    current_position = start_amount
    result = []
    for divisor in range(number_of_divisors):
        if current_position > ending_amount: break
        total += division_size
        result.append(total)
    return result

def compute_average(*args):
    sum = 0
    for argument in args: sum += argument
    average = sum/len(args)
    return average
