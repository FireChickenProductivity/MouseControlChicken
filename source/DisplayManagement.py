from .display.Display import Display
from .display.Canvas import Canvas
from .grid.Grid import Grid, Rectangle
from .SettingsMediator import settings_mediator
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
    def __init__(self, show_function, hide_function, cleanup_function=None):
        self.show_function = show_function
        self.hide_function = hide_function
        self.cleanup_function = cleanup_function
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
        if self.cleanup_function: self.cleanup_function()

    def is_flickering(self):
        return self.flickering

    def toggle_flickering(self, show_time: int, hide_time: int):
        if self.is_flickering():
            self.stop_flickering()
        else:
            self.start_flickering(show_time, hide_time)
    
    def is_flicker_showing(self) -> bool:
        return self.flicker_showing

class FlickererManager:
    def __init__(self, flickerers):
        self.flickerers = flickerers
    
    def cancel_all_flicker_jobs(self):
        for flickerer in self.flickerers:
            flickerer.cancel_flicker_job()

    def stop_all_flickering_except(self, exception_flickerer):
        for flickerer in self.flickerers:
            if flickerer != exception_flickerer:
                flickerer.stop_flickering()

    def restart_any_flickering(self):
        for flickerer in self.flickerers:
            if flickerer.is_flickering():
                flickerer.restart_flickering()

class DisplayManager:
    def __init__(self):
        self.display: Display = None
        self.is_showing: bool = False
        self.grid: Grid = None
        self.rectangle: Rectangle = None
        self.flickerer: Flickerer = Flickerer(self.flicker_show, self.hide_temporarily)
        self.transparency_flickerer: Flickerer = Flickerer(self.transparency_flicker_hide, self.transparency_flicker_show, settings_mediator.restore_transparency_settings)
        self.flickerer_manager: FlickererManager = FlickererManager([self.flickerer, self.transparency_flickerer])
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
        self.flickerer_manager.cancel_all_flicker_jobs()
    
    def show(self):
        if self.display: 
            self.show_temporarily()
            self.is_showing = True
            self.flickerer_manager.restart_any_flickering()
    
    def prepare_to_show(self):
        self.is_showing = True

    def hide_temporarily(self):
        if self.display: self.canvas.hide()
    
    def show_temporarily(self):
        if self.display: self.canvas.show()

    def refresh_canvas(self, rectangle: Rectangle):
        self.canvas = Canvas()
        self.canvas.setup(rectangle)
        self.display.draw_on(self.canvas)

    def refresh_display(self, grid: Grid, rectangle: Rectangle):
        self.hide_temporarily()
        self.display.set_grid(grid)
        self.display.set_rectangle(rectangle)
        if grid and rectangle: self.refresh_canvas(rectangle)
        self.grid = grid
        self.rectangle = rectangle
    
    def refresh_display_using_previous_values(self):
        self.refresh_display(self.grid, self.rectangle)

    def flicker_show(self):     
        self.refresh_display_using_previous_values()
        self.show_temporarily()

    def transparency_flicker_show(self):
        settings_mediator.rotate_transparency_settings_to_alternates()
        self.flicker_show()
    
    def transparency_flicker_hide(self):
        settings_mediator.restore_transparency_settings()
        self.flicker_show()

    def toggle_flickering(self, show_time: int, hide_time: int):
        self._toggle_flickering_for_flickerer(self.flickerer, show_time, hide_time)
    
    def toggle_transparency_flickering(self, show_time: int, hide_time: int):
        self._toggle_flickering_for_flickerer(self.transparency_flickerer, show_time, hide_time)
        
    def _toggle_flickering_for_flickerer(self, flickerer: Flickerer, show_time: int, hide_time: int):
        was_flickering = flickerer.is_flickering()
        self.flickerer_manager.stop_all_flickering_except(flickerer)
        flickerer.toggle_flickering(show_time, hide_time)
        if was_flickering:
            self.refresh_display_using_previous_values()
            self.show()

    def is_currently_showing(self) -> bool:
        return self.is_showing