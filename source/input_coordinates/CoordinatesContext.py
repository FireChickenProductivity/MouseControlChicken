from talon import Context

class CoordinateContext:
    def __init__(self, input_coordinate_capture_name: str, coordinate_level: int = 1):
        self.context = Context()
        self.tag = f"{input_coordinate_capture_name}_{coordinate_level}"
        self.input_coordinate_capture_name = input_coordinate_capture_name
        self.level = coordinate_level
        self.context.matches = f"""
        tag: user.{self.tag}
"""