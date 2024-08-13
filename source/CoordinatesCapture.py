from talon import Module, Context
from .InputCoordinateSystem import InputCoordinateSystem, InputCoordinateSystemCategory
from .grid.Grid import Grid
from .grid.GridCalculations import Node, compute_grid_tree

module = Module()
module.list('mouse_control_chicken_uppercase_letter', desc="Upper case letters for use with the mouse control chicken grids")

@module.capture(rule = "{user.mouse_control_chicken_uppercase_letter}")
def mouse_control_chicken_uppercase_letter(m) -> str:
    return m.mouse_control_chicken_uppercase_letter

@module.capture(rule = "(<user.letter>|<user.mouse_control_chicken_uppercase_letter>|<number_small>)+")
def mouse_control_chicken_coordinates(m) -> str:
    result: str = ""
    after_first_element: bool = False
    for element in m: 
        if after_first_element:
            result += " "
        else:
            after_first_element = True
        result += str(element)
    return result

module.list('mouse_control_chicken_empty_list', desc="An empty list")

@module.capture(rule = "<number_small>+")
def mouse_control_chicken_number_sequence(m) -> str:
    return " ".join([str(x) for x in m])

@module.capture(rule = "<number_small>")
def mouse_control_chicken_single_number(m) -> str:
    return str(m[0])

@module.capture(rule = "<user.letter> <user.letter>")
def mouse_control_chicken_lowercase_letter_pair(m) -> str:
    return m[0] + " " + m[1]

@module.capture(rule = "<user.letter>|<user.mouse_control_chicken_uppercase_letter>")
def mouse_control_chicken_letter(m) -> str:
    return m[0]

@module.capture(rule = "<user.mouse_control_chicken_letter> <user.mouse_control_chicken_letter>")
def mouse_control_chicken_letter_pair(m) -> str:
    return m[0] + " " + m[1] 

@module.capture(rule = "<user.mouse_control_chicken_letter_pair>")
def mouse_control_chicken_main_coordinates(m) -> str:
    return " ".join(m)

@module.capture(rule = "<user.letter> <user.letter>")
def mouse_control_chickens_secondary_coordinates(m) -> str:
    return " ".join(m)

@module.capture(rule = "<user.mouse_control_chicken_letter_pair>")
def mouse_control_chicken_tertiary_coordinates(m) -> str:
    return " ".join(m)

class CoordinateContext:
    def __init__(self, input_coordinate_capture_name: str, coordinate_level: int = 1):
        self.context = Context()
        self.tag = f"{input_coordinate_capture_name}_{coordinate_level}"
        self.context.matches = f"""
        tag: user.{self.tag}
"""
        
override_contexts = []
def build_override_contexts():
    input_coordinate_capture_names = ["mouse_control_chicken_number_sequence", "mouse_control_chicken_lowercase_letter_pair", "mouse_control_chicken_letter_pair", "mouse_control_chicken_single_number"]
    captures_to_override_by_level = {1:"mouse_control_chicken_main_coordinates", 2:"mouse_control_chickens_secondary_coordinates", 3:"mouse_control_chicken_tertiary_coordinates"}
    for input_coordinate_capture_name in input_coordinate_capture_names:
        for level, capture_to_override in captures_to_override_by_level.items():
            context = CoordinateContext(input_coordinate_capture_name, level)
            @context.context.capture("user." + capture_to_override, rule = f"<user.{input_coordinate_capture_name}>")
            def new_capture(m) -> str:
                text_list = [str(e) for e in m]
                return " ".join(text_list)
            module.tag(context.tag, desc=f"Tag for the level {level} of the {input_coordinate_capture_name} capture")
            override_contexts.append(context)
build_override_contexts()

def compute_tag_start_for_category(category: InputCoordinateSystemCategory):
    result = ""
    if category == InputCoordinateSystemCategory.LETTER_PAIR:
        result = "letter_pair"
    elif category == InputCoordinateSystemCategory.NUMBER_SEQUENCE:
        result = "number_sequence"
    elif category == InputCoordinateSystemCategory.SINGLE_NUMBER:
        result = "single_number"
    elif category == InputCoordinateSystemCategory.LOWERCASE_LETTER_PAIR:
        result = "lowercase_letter_pair"
    if result:
        result = f"mouse_control_chicken_{result}"
    return result

def compute_tag_for_coordinate_system_category_and_depth(category: InputCoordinateSystemCategory, depth: int) -> str:
    category_tag_start = compute_tag_start_for_category(category)
    if not category_tag_start:
        return None
    return f"user.{category_tag_start}_{depth}"

def compute_categories(grid: Grid):
    result = []
    tree = compute_grid_tree(grid)
    while tree:
        node_grid = tree.get_value()
        coordinate_system = node_grid.get_coordinate_system()
        category = coordinate_system.get_category()
        result.append(category)
        print('category', category)
        if tree.has_children():
            tree = tree.get_children()[0]
        else:
            tree = None
    print('categories', result)
    return result

def compute_category_tags(grid: Grid):
    categories = compute_categories(grid)
    result = []
    for index, category in enumerate(categories):
        tag = compute_tag_for_coordinate_system_category_and_depth(category, index + 1)
        if tag:
            result.append(tag)  
    print('category tags', result)
    return result
