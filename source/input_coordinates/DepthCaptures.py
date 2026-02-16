#This defines captures for handling grade composition depth
from talon import Module, Context
from .Captures import compute_coordinates_from_utterance

module = Module()

#The maximum level of composition supported
DEPTH_LIMIT = 3

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
    for level in range(1, DEPTH_LIMIT + 1):
        context = LevelContext(level)
        module.tag(context.tag, desc=f"Tag for a mouse control chicken coordinate system coordinate system with depth {level}.")
        level_contexts.append(context)
build_level_contexts()

@level_contexts[0].context.capture("user.mouse_control_chicken_coordinates", rule = "<user.mouse_control_chicken_main_coordinates>")
def mouse_control_chicken_level_one_coordinates(m) -> str:
    return compute_coordinates_from_utterance(m)

@level_contexts[1].context.capture(
    "user.mouse_control_chicken_coordinates",
    rule = "(<user.mouse_control_chicken_main_coordinates> [<user.mouse_control_chicken_secondary_coordinates>])|<user.mouse_control_chicken_secondary_coordinates>"
    )
def mouse_control_chicken_level_two_coordinates(m) -> str:
    return compute_coordinates_from_utterance(m)

@level_contexts[2].context.capture(
    "user.mouse_control_chicken_coordinates",
    rule = "(<user.mouse_control_chicken_main_coordinates> [<user.mouse_control_chicken_secondary_coordinates> [<user.mouse_control_chicken_tertiary_coordinates>]])|(<user.mouse_control_chicken_secondary_coordinates> [<user.mouse_control_chicken_tertiary_coordinates>])|<user.mouse_control_chicken_tertiary_coordinates>"
    )
def mouse_control_chicken_level_three_coordinates(m) -> str:
    return compute_coordinates_from_utterance(m)