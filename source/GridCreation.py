from .GridOptions import GridOption
from .FileUtilities import mouse_control_chicken_write_grid_option
from talon import Module, actions

class CurrentGrid:
    def __init__(self):
        self.name = ''
        self.factory_name = ''
        self.arguments = ''
        self.default_display_name = ''
    
    def set_name(self, name: str):
        self.name = name

    def set_factory_name(self, factory_name: str):
        self.factory_name = factory_name
    
    def set_arguments(self, arguments: str):
        self.arguments = arguments

    def set_default_display_name(self, default_display_name: str):
        self.default_display_name = default_display_name
    
    def get_name(self) -> str:
        return self.name

    def get_factory_name(self) -> str:
        return self.factory_name

    def get_arguments(self) -> str:
        return self.arguments
    
    def get_default_display_name(self) -> str:
        return self.default_display_name
    
    def compute_grid_option(self) -> GridOption:
        return GridOption(self.name, self.factory_name, self.default_display_name, self.arguments)

current_grid: CurrentGrid = None

module = Module()
@module.action_class
class Actions:
    def mouse_control_chickens_start_creating_new_grid():
        """Starts creating a new mouse control chicken grid"""
        global current_grid
        current_grid = CurrentGrid()
        actions.user.mouse_control_chicken_enable_grid_creation_tag()
        actions.user.mouse_control_chicken_show_dictation_input_display_with_title_acceptance_callback_and_cancellation_callback(
            "Choose Grid Name: say choose <grid name>",
            actions.user.mouse_control_chicken_set_current_grid_name,
            actions.user.mouse_control_chicken_cancel_grid_creation
        )

    def mouse_control_chicken_set_current_grid_name(name: str):
        """Sets the name of the current mouse control chicken grid under construction"""
        global current_grid
        current_grid.set_name(name)
    
    def mouse_control_chicken_set_current_grid_factory_name(factory_name: str):
        """Sets the factory name of the current mouse control chicken grid under construction"""
        global current_grid
        current_grid.set_factory_name(factory_name)
    
    def mouse_control_chicken_set_current_grid_arguments(arguments: str):
        """Sets the arguments of the current mouse control chicken grid under construction"""
        global current_grid
        current_grid.set_arguments(arguments)
    
    def mouse_control_chicken_set_current_grid_default_display_name(default_display_name: str):
        """Sets the default display name of the current mouse control chicken grid under construction"""
        global current_grid
        current_grid.set_default_display_name(default_display_name)
    
    def mouse_control_chicken_finish_creating_new_grid():
        """Finishes creating a new mouse control chicken grid"""
        actions.user.mouse_control_chicken_disable_grid_creation_tag()
        global current_grid
        mouse_control_chicken_write_grid_option(current_grid.compute_grid_option())
        current_grid = None

    def mouse_control_chicken_cancel_grid_creation():
        """Cancels the creation of a new mouse control chicken grid"""
        actions.user.mouse_control_chicken_disable_grid_creation_tag()
        global current_grid
        current_grid = None
        print('cancelled')