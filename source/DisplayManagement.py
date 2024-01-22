from .display.Display import Display
from .Grid import Grid, Rectangle
from talon import cron

class DisplayManager:
    def __init__(self):
        self.display: Display = None
        self.is_showing: bool = False
        self.flicker_job = None
        self.is_flickering: bool = False
        self.flicker_show_time: int = None
        self.flicker_hide_time: int = None
    
    def set_display(self, display: Display):
        self.hide()
        self.display = display
    
    def get_display(self) -> Display:
        return self.display

    def has_display(self) -> bool:
        return self.display is not None
    
    def hide(self):
        self.hide_temporarily()
        self.is_showing = False
    
    def show(self):
        if self.display: 
            self.show_temporarily()
            self.is_showing = True
            if self.is_flickering:
                self.start_flickering(self.flicker_show_time, self.flicker_hide_time)
        
    def hide_temporarily(self):
        if self.display: self.display.hide()
    
    def show_temporarily(self):
        if self.display: self.display.show()

    def refresh_display(self, grid: Grid, rectangle: Rectangle):
        self.display.set_grid(grid)
        self.display.set_rectangle(rectangle)
        self.display.show()
    
    def toggle(self):
        if self.is_showing:
            self.hide()
        else:
            self.show()

    def flicker_show(self):
        self.show_temporarily()
        self.flicker_job = cron.after(f'{self.flicker_showtime}ms', lambda: self.flicker_hide())

    def flicker_hide(self):
        self.hide_temporarily()
        self.flicker_job = cron.after(f'{self.flicker_hide_time}ms', lambda: self.flicker_show())

    def start_flickering(self, showtime: int, hidetime: int):
        self.flicker_show_time = showtime
        self.flicker_hide_time = hidetime
        if self.flicker_job:
            self.flicker_job.cancel()
        self.flicker_show()
        self.is_flickering = True
    
    def stop_flickering(self):      
        if self.flicker_job:
            self.flicker_job.cancel()
            self.flicker_job = None
        self.is_flickering = False
        
    