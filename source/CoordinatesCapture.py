from talon import Module

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
def mouse_control_chicken_number_sequence(m) -> int:
    return int(" ".join([str(x) for x in m]))

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