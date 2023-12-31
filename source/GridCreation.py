from .Grid import Grid
from .GridOptions import GridOption
from .GridFactory import GridFactory, GRID_ARGUMENT_SEPARATOR
from .GridFactoryArgumentTypes import FactoryArgumentType
from .Display.DisplayOptionsComputer import compute_display_options_names_given_grid
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

    def compute_grid(self) -> Grid:
        return actions.user.mouse_control_chicken_create_grid_from_factory(self.factory_name, self.arguments)

class ArgumentBuilder:
    def __init__(self, factory: GridFactory):
        self.factory = factory
        self.arguments = []
        self.argument_index = 0

    def obtain_next_argument_from_user(self):
        argument_types = self.factory.get_argument_types()
        if self.argument_index >= len(argument_types):
            self.handle_having_obtained_all_arguments()
        else:
            self.handle_argument_type(argument_types[self.argument_index])

    def handle_argument_type(self, argument_type: FactoryArgumentType):
        if argument_type.supports_options_dialogue():
            self.handle_obtaining_argument_with_options_dialogue(argument_type)
        else:
            self.handle_obtaining_argument_without_options_dialogue(argument_type)
        
    def handle_obtaining_argument_with_options_dialogue(self, argument_type: FactoryArgumentType):
        def handle_choice(choice: str):
            self.argument_index += 1
            self.arguments.append(choice)
            self.obtain_next_argument_from_user()
        actions.user.mouse_control_chicken_show_dictation_input_dialogue_with_title_acceptance_callback_cancellation_callback_tag_names_and_options(
            f"Choose argument {self.argument_index + 1}. Arguments description: {self.factory.get_arguments_description()}: say choose <argument number>",
            handle_choice,
            actions.user.mouse_control_chicken_cancel_grid_creation,
            argument_type.get_tags(),
            argument_type.get_options()
        )

    def handle_obtaining_argument_without_options_dialogue(self, argument_type: FactoryArgumentType):
        def handle_argument(argument):
            self.argument_index += 1
            self.arguments.append(str(argument))
            self.obtain_next_argument_from_user()
        actions.user.mouse_control_chicken_show_dictation_input_dialogue_with_title_acceptance_callback_cancellation_callback_and_tag_names(
            f"Choose argument {self.argument_index + 1}. Arguments description: {self.factory.get_arguments_description()}: say choose <argument>",
            handle_argument,
            actions.user.mouse_control_chicken_cancel_grid_creation,
            argument_type.get_tags()
        )

    def handle_having_obtained_all_arguments(self):
        argument: str = GRID_ARGUMENT_SEPARATOR.join(self.arguments)
        actions.user.mouse_control_chicken_set_current_grid_arguments(argument)
        actions.user.mouse_control_chickens_start_default_display_name_selection()

    

current_grid: CurrentGrid = None

module = Module()
@module.action_class
class Actions:
    def mouse_control_chickens_start_creating_new_grid():
        """Starts creating a new mouse control chicken grid"""
        global current_grid
        current_grid = CurrentGrid()
        actions.user.mouse_control_chicken_enable_grid_creation_tag()
        def handle_accepting_dictation_input(dictation_input: str):
            actions.user.mouse_control_chicken_set_current_grid_name(dictation_input)
            actions.user.mouse_control_chicken_start_grid_factory_selection()
        actions.user.mouse_control_chicken_show_dictation_input_dialogue_with_title_acceptance_callback_and_cancellation_callback(
            "Choose Grid Name: say choose <grid name>",
            handle_accepting_dictation_input,
            actions.user.mouse_control_chicken_cancel_grid_creation
        )

    def mouse_control_chicken_start_grid_factory_selection():
        """Shows the dialogue for selecting a mouse control chicken grid factory to use to create the current grid"""
        def handle_choice(choice: str):
            actions.user.mouse_control_chicken_set_current_grid_factory_name(choice)
            actions.user.mouse_control_chicken_start_grid_argument_selection()
        actions.user.mouse_control_chicken_show_dictation_input_dialogue_with_title_acceptance_callback_cancellation_callback_and_options(
            "Choose Grid Factory: say choose <grid factory number>",
            handle_choice,
            actions.user.mouse_control_chicken_cancel_grid_creation,
            actions.user.mouse_control_chicken_get_grid_factory_options()
        )

    def mouse_control_chicken_start_grid_argument_selection():
        """Shows the dialogue for selecting the arguments to use to create the current grid"""
        factory_name = current_grid.get_factory_name()
        factory: GridFactory = actions.user.mouse_control_chicken_get_grid_factory(factory_name)
        builder: ArgumentBuilder = ArgumentBuilder(factory)
        builder.obtain_next_argument_from_user()
        
    def mouse_control_chickens_start_default_display_name_selection():
        """Shows the dialogue for selecting the default display name for the current grid"""
        def handle_choice(choice: str):
            actions.user.mouse_control_chicken_set_current_grid_default_display_name(choice)
            actions.user.mouse_control_chicken_finish_creating_new_grid()
        actions.user.mouse_control_chicken_show_dictation_input_dialogue_with_title_acceptance_callback_cancellation_callback_and_options(
            "Choose Default Display: say choose <display number>",
            handle_choice,
            actions.user.mouse_control_chicken_cancel_grid_creation,
            compute_display_options_names_given_grid(current_grid.compute_grid())
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