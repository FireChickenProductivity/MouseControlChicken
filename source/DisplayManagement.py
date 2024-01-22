from .display.Display import Display
from talon import cron

class DisplayManager:
    def __init__(self):
        self.display: Display = None
        self.is_showing: bool = False
        self.flicker_job = None
    
    def set_display(self, display: Display):
        self.hide()
        self.display = display
    
    def get_display(self) -> Display:
        return self.display
    
    def hide(self):
        if self.display: self.display.hide()
        self.is_showing = False
    
    def show(self):
        if self.display: 
            self.display.show()
            self.is_showing = True
    
    def toggle(self):
        if self.is_showing:
            self.hide()
        else:
            self.show()


    def flicker_show(self, showtime: int, hidetime: int):
        self.show()
        self.flicker_job = cron.after(f'{showtime}ms', lambda: self.flicker_hide(showtime, hidetime))

    def flicker_hide(self, showtime: int, hidetime: int):
        self.hide()
        self.flicker_job = cron.after(f'{hidetime}ms', lambda: self.flicker_show(showtime, hidetime))

    def start_flickering(self, showtime: int, hidetime: int):
        if self.flicker_job:
            self.flicker_job.cancel()
        self.flicker_show(showtime, hidetime)
    
    def stop_flickering(self):      
        if self.flicker_job:
            self.flicker_job.cancel()
            self.flicker_job = None
        
    