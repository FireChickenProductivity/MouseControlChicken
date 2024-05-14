from talon import actions

class DialogueOptions:
    def __init__(self, callback_function, title = "", cancellation_function = None, options = None):
        self.callback_function = callback_function
        self.cancellation_function = cancellation_function
        if not cancellation_function:
            self.cancellation_function = lambda: None
        self.title = title
        self.options = options
    
    def handle_choice(self, choice: str):
        self.callback_function(choice)
    
    def handle_cancellation(self):
        self.cancellation_function()
    
    def get_title(self):
        return self.title
    
    def get_options(self):
        return self.options