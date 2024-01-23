from .display.Display import Display
from .Grid import Grid, Rectangle
from talon import cron

class Flickerer:
    def __init__(self, show_function, hide_function):
        self.show_function = show_function
        self.hide_function = hide_function
        self.flicker_job = None
        self.flickering = False
        self.flicker_show_time = None
        self.flicker_hide_time = None
        self.secondary_flicker_job = None
    
    def cancel_flicker_job(self):
        if self.flicker_job:
            cron.cancel(self.flicker_job)
            self.flicker_job = None
            cron.cancel(self.secondary_flicker_job)
            self.secondary_flicker_job = None
    
    def flicker_show(self):
        self.show_function()
        self.secondary_flicker_job = cron.after(f'{self.flicker_show_time}ms', self.hide_function) 

    def start_flickering(self, showtime: int, hidetime: int):
        self.cancel_flicker_job()
        self.flicker_show_time = showtime
        self.flicker_hide_time = hidetime
        self.flicker_show()
        self.flickering = True
        self.flicker_job = cron.interval(f'{self.flicker_show_time + self.flicker_hide_time}ms', self.flicker_show)

    def restart_flickering(self):
        self.start_flickering(self.flicker_show_time, self.flicker_hide_time)

    def stop_flickering(self):
        self.cancel_flicker_job()
        self.flickering = False

    def is_flickering(self):
        return self.flickering

class DisplayManager:
    def __init__(self):
        self.display: Display = None
        self.is_showing: bool = False
        self.grid: Grid = None
        self.rectangle: Rectangle = None
        self.flickerer: Flickerer = Flickerer(self.flicker_show, self.hide_temporarily)
    
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
        self.flickerer.cancel_flicker_job()
    
    def show(self):
        if self.display: 
            self.show_temporarily()
            self.is_showing = True
            if self.flickerer.is_flickering():
                self.flickerer.restart_flickering()
        
    def hide_temporarily(self):
        if self.display: self.display.hide()
    
    def show_temporarily(self):
        if self.display: self.display.show()

    def refresh_display(self, grid: Grid, rectangle: Rectangle):
        self.display.set_grid(grid)
        self.display.set_rectangle(rectangle)
        self.grid = grid
        self.rectangle = rectangle
    
    def toggle(self):
        if self.is_showing:
            self.hide()
        else:
            self.show()

    def flicker_show(self):
        self.refresh_display(self.grid, self.rectangle)
        self.show_temporarily()

    def start_flickering(self, showtime: int, hidetime: int):
        self.flickerer.start_flickering(showtime, hidetime)
    
    def stop_flickering(self):      
        self.flickerer.stop_flickering()
        
    