#Defines captures for the input coordinates grammar

from talon import Module, Context

module = Module()
default_context = Context()

#Define lists representing specific kinds of coordinates
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
    result["ten"] = "10"
    for ten_product in tens:
        result[ten_product] = str(tens[ten_product])
        for digit in digits:
            result[f"{ten_product} {digit}"] = str(tens[ten_product] + digits[digit])
    return result

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
def mouse_control_chicken_secondary_coordinates(m) -> str:
    return " ".join(m)

@module.capture(rule = "<user.mouse_control_chicken_letter_pair>")
def mouse_control_chicken_tertiary_coordinates(m) -> str:
    return " ".join(m)