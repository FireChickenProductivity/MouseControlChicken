from talon import Module, Context
from .InputCoordinateSystem import InputCoordinateSystem, InputCoordinateSystemCategory
from .grid.Grid import Grid
from .grid.GridCalculations import Node, compute_grid_tree, TreeComputationOptions

module = Module()
module.list('mouse_control_chicken_uppercase_letter', desc="Upper case letters for use with the mouse control chicken grids")
module.list('mouse_control_chicken_number_small', desc="Numeric coordinates for mouse control chicken")

def create_custom_number_small():
    result = {}
    digits = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
    eleven_to_nineteen = {"eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19}
    tens = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
    for digit in digits:
        result[digit] = str(digits[digit])
    for number in eleven_to_nineteen:
        result[number] = str(eleven_to_nineteen[number])
    for ten_product in tens:
        for digit in digits:
            result[f"{ten_product} {digit}"] = str(tens[ten_product] + digits[digit])
    return result

default_context = Context()
default_context.lists["user.mouse_control_chicken_number_small"] = create_custom_number_small()

@module.capture(rule = "{user.mouse_control_chicken_uppercase_letter}")
def mouse_control_chicken_uppercase_letter(m) -> str:
    return m.mouse_control_chicken_uppercase_letter

def compute_coordinates_from_utterance(m) -> str:
    result: str = ""
    after_first_element: bool = False
    for element in m: 
        if after_first_element:
            result += " "
        else:
            after_first_element = True
        result += str(element)
    return result

@module.capture(rule = "(<user.letter>|<user.mouse_control_chicken_uppercase_letter>|{user.mouse_control_chicken_number_small})+")
def mouse_control_chicken_coordinates(m) -> str:
    return compute_coordinates_from_utterance(m)

module.list('mouse_control_chicken_empty_list', desc="An empty list")

@module.capture(rule = "{user.mouse_control_chicken_number_small}+")
def mouse_control_chicken_number_sequence(m) -> str:
    return " ".join([str(x) for x in m])

@module.capture(rule = "{user.mouse_control_chicken_number_small}")
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

def compute_level_tag(level: int) -> str:
    return f"mouse_control_chicken_coordinate_system_level_{level}"

class LevelContext:
    def __init__(self, level: int):
        self.context = Context()
        self.tag = compute_level_tag(level)
        self.context.matches = f"""
        tag: user.{self.tag}
"""

level_contexts = []
def build_level_contexts():
    for level in range(1, 4):
        context = LevelContext(level)
        module.tag(context.tag, desc=f"Tag for a mouse control chicken coordinate system coordinate system with depth {level}.")
        level_contexts.append(context)
build_level_contexts()

@level_contexts[0].context.capture("user.mouse_control_chicken_coordinates", rule = "<user.mouse_control_chicken_main_coordinates>")
def mouse_control_chicken_level_one_coordinates(m) -> str:
    return compute_coordinates_from_utterance(m)

@level_contexts[1].context.capture(
    "user.mouse_control_chicken_coordinates",
    rule = "(<user.mouse_control_chicken_main_coordinates> [<user.mouse_control_chickens_secondary_coordinates>])|<user.mouse_control_chickens_secondary_coordinates>"
    )
def mouse_control_chicken_level_two_coordinates(m) -> str:
    return compute_coordinates_from_utterance(m)

@level_contexts[2].context.capture(
    "user.mouse_control_chicken_coordinates",
    rule = "(<user.mouse_control_chicken_main_coordinates> [<user.mouse_control_chickens_secondary_coordinates> [<user.mouse_control_chicken_tertiary_coordinates>]])|(<user.mouse_control_chickens_secondary_coordinates> [<user.mouse_control_chicken_tertiary_coordinates>])|<user.mouse_control_chicken_tertiary_coordinates>"
    )
def mouse_control_chicken_level_three_coordinates(m) -> str:
    return compute_coordinates_from_utterance(m)

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

def _append_tree_node_category_to_list(tree: Node, input_list: list):
    number_of_children = len(tree.get_children())
    if number_of_children < 2:
        node_grid = tree.get_value()
        coordinate_system = node_grid.get_coordinate_system()
        category = coordinate_system.get_category()
        input_list.append(category)

def compute_categories(grid: Grid):
    result = []
    tree_computation_options = TreeComputationOptions(keep_coordinate_system_modifying_wrappers=True)
    tree = compute_grid_tree(grid, tree_computation_options)
    while tree:
        _append_tree_node_category_to_list(tree, result)
        if tree.has_children():
            tree = tree.get_children()[0]
        else:
            tree = None
    return result

def compute_category_tags(grid: Grid):
    categories = compute_categories(grid)
    result = []
    for index, category in enumerate(categories):
        tag = compute_tag_for_coordinate_system_category_and_depth(category, index + 1)
        if tag:
            result.append(tag)  
    return result


def compute_level_for_tag(tag: str) -> int:
    last_underscore_index = tag.rfind("_")
    if last_underscore_index == -1:
        return 0
    level_text = tag[last_underscore_index + 1:]
    level = int(level_text)
    return level

def compute_appropriate_level_tag_from_category_tags(category_tags):
    maximum_level = 0
    for tag in category_tags:
        level = compute_level_for_tag(tag)
        if level > maximum_level:
            maximum_level = level
    if maximum_level > 0 and maximum_level < 4:
        return 'user.' + compute_level_tag(maximum_level)
    return None
