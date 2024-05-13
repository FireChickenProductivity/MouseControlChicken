from talon import actions
from ..display.DisplayOptionsComputations import compute_display_options_separated_by_index_for_grid, DISPLAY_NAME_SEPARATOR
from ..grid.Grid import Grid
from .DialogueOptions import DialogueOptions

def show_combination_display_options(dialogue_options: DialogueOptions, grid: Grid, index: int = 0, combination_display_name: str = ""):
    options = compute_display_options_separated_by_index_for_grid(grid)
    if index >= len(options):
        dialogue_options.handle_choice(combination_display_name)
    else:
        options_text = [option.get_display_name() for option in options[index]]
        def update_combination_display_name(name: str):
            nonlocal combination_display_name
            if combination_display_name:
                combination_display_name += DISPLAY_NAME_SEPARATOR
            combination_display_name += name
            show_combination_display_options(dialogue_options, grid, index + 1, combination_display_name)
        if len(options_text) == 1:
            update_combination_display_name(options_text[0])
        else:
            actions.user.mouse_control_chicken_show_dictation_input_dialogue_with_title_acceptance_callback_cancellation_callback_and_options(
            str(index + 1) + "|" + dialogue_options.get_title(),
            update_combination_display_name,
            dialogue_options.handle_cancellation,
            options_text,
            )

