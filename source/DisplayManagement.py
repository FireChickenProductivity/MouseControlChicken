from .display.Display import Display
from .display.Canvas import Canvas
from .Grid import Grid, Rectangle
from talon import cron

class JobHandler:
    def __init__(self):
        self.job = None
    
    def set_job(self, job):
        self.job = job
    
    def cancel_job(self):
        if self.job:
            cron.cancel(self.job)
            self.job = None

class Flickerer:
    def __init__(self, show_function, hide_function):
        self.show_function = show_function
        self.hide_function = hide_function
        self.flicker_job_handler = JobHandler()
        self.flickering = False
        self.flicker_show_time = None
        self.flicker_hide_time = None
        self.secondary_flicker_job_handler = JobHandler()
        self.flicker_showing = False
    
    def cancel_flicker_job(self):
        self.flicker_job_handler.cancel_job()
        self.secondary_flicker_job_handler.cancel_job()
    
    def flicker_hide(self):
        self.flicker_showing = False
        self.hide_function()    

    def flicker_show(self):
        self.show_function()
        self.flicker_showing = True
        hide_job = cron.after(f'{self.flicker_show_time}ms', self.flicker_hide) 
        self.secondary_flicker_job_handler.set_job(hide_job)

    def start_flickering(self, showtime: int, hidetime: int):
        self.cancel_flicker_job()
        self.flicker_show_time = showtime
        self.flicker_hide_time = hidetime
        self.flicker_show()
        self.flickering = True
        flicker_job = cron.interval(f'{self.flicker_show_time + self.flicker_hide_time}ms', self.flicker_show)
        self.flicker_job_handler.set_job(flicker_job)

    def restart_flickering(self):
        self.start_flickering(self.flicker_show_time, self.flicker_hide_time)

    def stop_flickering(self):
        self.cancel_flicker_job()
        self.flickering = False

    def is_flickering(self):
        return self.flickering

    def toggle_flickering(self, show_time: int, hide_time: int):
        if self.is_flickering():
            self.stop_flickering()
        else:
            self.start_flickering(show_time, hide_time)
    
    def is_flicker_showing(self) -> bool:
        return self.flicker_showing

class DisplayManager:
    def __init__(self):
        self.display: Display = None
        self.is_showing: bool = False
        self.grid: Grid = None
        self.rectangle: Rectangle = None
        self.flickerer: Flickerer = Flickerer(self.flicker_show, self.hide_temporarily)
        self.canvas: Canvas = Canvas()
    
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
        if self.display: self.canvas.hide()
    
    def show_temporarily(self):
        if self.display: self.canvas.show()

    def reset_canvas(self):
        self.canvas = Canvas()

    def refresh_display(self, grid: Grid, rectangle: Rectangle):
        self.hide()
        self.display.set_grid(grid)
        self.display.set_rectangle(rectangle)
        if grid and rectangle:
            self.reset_canvas()
            self.canvas.setup(rectangle)
            self.display.draw_on(self.canvas)
        self.grid = grid
        self.rectangle = rectangle
    
    def toggle(self):
        if self.is_showing:
            self.hide()
        else:
            self.show()

    def refresh_display_using_previous_values(self):
        self.refresh_display(self.grid, self.rectangle)

    def flicker_show(self):
        self.refresh_display_using_previous_values()
        self.show_temporarily()

    def toggle_flickering(self, show_time: int, hide_time: int):
        self.flickerer.toggle_flickering(show_time, hide_time)
        if not self.flickerer.is_flicker_showing():
            self.refresh_display_using_previous_values()
            self.show()