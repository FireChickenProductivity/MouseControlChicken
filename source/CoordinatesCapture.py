from talon import Module

module = Module()
@module.capture(rule = "({user.letter}|<number>)+")
def mouse_control_chicken_coordinates(m) -> str:
    result: str = ""
    for element in m: result += str(element)
    return result