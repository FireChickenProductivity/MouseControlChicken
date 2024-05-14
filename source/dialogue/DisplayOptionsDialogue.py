from talon import actions
from ..display.DisplayOptionsComputations import compute_display_options_separated_by_index_for_grid, DISPLAY_NAME_SEPARATOR
from ..grid.Grid import Grid
from .DialogueOptions import DialogueOptions

def show_combination_display_options(
    dialogue_options: DialogueOptions,
    grid: Grid
):
    manager = CombinationDisplayOptionsManager(dialogue_options, grid)
    manager.show_combination_display_options()

class CombinationDisplayOptionsManager:
    def __init__(self, dialogue_options: DialogueOptions,
    grid: Grid):
        self.dialogue_options = dialogue_options
        self.grid = grid
        self.options = compute_display_options_separated_by_index_for_grid(grid)
        self.index = 0
        self.combination_display_name = ""
    
    def show_combination_display_options(self):
        if self.index >= len(self.options):
            self.dialogue_options.handle_choice(self.combination_display_name)
        else:
            self.show_combination_display_options_recursively()
        
    def show_combination_display_options_recursively(self):
        options_text = [option.get_display_name() for option in self.options[self.index]]
        if len(options_text) == 1:
            self.update_combination_display_name(options_text[0])
        else:
            actions.user.mouse_control_chicken_show_dictation_input_dialogue_with_title_acceptance_callback_cancellation_callback_and_options(
            str(self.index + 1) + "|" + self.dialogue_options.get_title(),
            self.update_combination_display_name,
            self.dialogue_options.handle_cancellation,
            options_text,
            )
            
    def update_combination_display_name(self, name: str):
        if self.combination_display_name:
            self.combination_display_name += DISPLAY_NAME_SEPARATOR
        self.combination_display_name += name
        self.index += 1
        self.show_combination_display_options()