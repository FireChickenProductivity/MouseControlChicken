from talon import Module

module = Module()
@module.capture(rule = "({user.letter}|<number_small>)+")
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