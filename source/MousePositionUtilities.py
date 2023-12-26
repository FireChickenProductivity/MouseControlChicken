from .fire_chicken.mouse_position import MousePosition

def compute_mouse_position_average(start: MousePosition, ending: MousePosition) -> MousePosition:
    return 0.5*(start + ending)