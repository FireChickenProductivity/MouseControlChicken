def convert_color_name_to_hexadecimal_color_code(name):
    color_name_to_hexadecimal_color_code = {
        'black': '#000000',
        'blue': '#0000FF',
        'green': '#008000',
        'red': '#FF0000',
        'white': '#FFFFFF',
        'yellow': '#FFFF00',
        'bright green': '#66ff00',
        'bright blue': '#0096FF',
    }
    return color_name_to_hexadecimal_color_code.get(name, None)

def compute_color(text: str) -> str:
    color = convert_color_name_to_hexadecimal_color_code(text)
    if color is not None:
        return color
    return text