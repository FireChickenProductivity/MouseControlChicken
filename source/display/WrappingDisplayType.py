class WrappingDisplayType:
    def __init__(self, wrapper, wrapped):
        self.wrapper = wrapper
        self.wrapped = wrapped
    
    def __call__(self):
        return self.wrapper(self.wrapped())
    
    def get_name(self) -> str:
        return self.__call__().get_name()

    def get_wrapped(self):
        return self.wrapped