#This will need to respond to on inclusion and generate positions
#Or just compute offset amount

class ZigzagOffsetComputer:
    def __init__(self, offset_unit: int, return_threshold: int, direction: int = 1):
        self.offset_unit = offset_unit
        self.return_threshold = return_threshold
        self.offset = 0
        self.change_amount = 1
        self.direction = direction
    
    def compute_offset(self):
        return self.offset*self.offset_unit
    
    def update_offset(self):
        self.offset += self.change_amount*self.direction
        if self.offset == self.return_threshold or self.offset == 0:
            self.change_amount *= -1
    