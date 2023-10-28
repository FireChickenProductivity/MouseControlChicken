from .Grid import Grid, Rectangle

class Display:
    def set_grid(grid: Grid): pass
    def set_rectangle(rectangle: Rectangle): pass
    def show(): pass
    def hide(): pass
    def refresh(): pass


class FrameDisplay(Display): 
    '''Displays a grid around a rectangle showing the coordinates of the grid'''
    pass

class CrisscrossDisplay(Display):
    '''Displays a grid within a rectangle by showing positions on the grade with criss crossing horizontal and vertical lines'''
    pass

