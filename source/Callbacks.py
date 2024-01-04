class Callback:
    def __init__(self, callback_function, un_registration_callback_function = None):
        self.callback_function = callback_function
        self.un_registration_callback_function = un_registration_callback_function
    
    def call(self, *args):
        self.callback_function(*args)
    
    def handle_un_registration(self):
        if self.un_registration_callback_function:
            self.un_registration_callback_function(self)

class NoArgumentCallback(Callback):
    def call(self, *args):
        self.callback_function()
        
class CallbackManager:
    def __init__(self):
        self.callbacks = {}
    
    def register_callback(self, name: str, callback: Callback):
        if name in self.callbacks:
            self.unregister_callback(name)
        self.callbacks[name] = callback
    
    def unregister_callback(self, name: str):
        current_callback = self.callbacks[name]
        current_callback.handle_un_registration()
        del self.callbacks[name]

    def has_callback(self, name: str) -> bool:
        return name in self.callbacks

    def call_callback(self, name: str, *args):
        if self.has_callback(name):
            self.callbacks[name].call(*args)
    
    def call_callbacks(self, *args):
        for callback in self.callbacks.values():
            callback.call(*args)
