from talon import Module, Context

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
        self.context.matches = f"""
        tag: user.{input_coordinate_capture_name}_{coordinate_level}
"""
        
override_contexts = []
def build_override_contexts():
    input_coordinate_capture_names = ["mouse_control_chicken_number_sequence", "mouse_control_chicken_lowercase_letter_pair", "mouse_control_chicken_letter_pair", "mouse_control_chicken_single_number"]
    captures_to_override_by_level = {1: ["mouse_control_chicken_main_coordinates"], 2: ["mouse_control_chickens_secondary_coordinates"], 3: ["mouse_control_chicken_tertiary_coordinates"]}

