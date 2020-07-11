from kivy.app import App  
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import kivy.properties as kv
class MainWidget(BoxLayout): 
      
    number = kv.NumericProperty() 
      
    def __init__(self, **kwargs): 
        super(MainWidget, self).__init__(**kwargs)
        
        
    def increment_time(self, interval): 
        self.number += .1
    def start(self): 
        Clock.unschedule(self.increment_time) 
        Clock.schedule_interval(self.increment_time, .1)
    def stop(self): 
        Clock.unschedule(self.increment_time)

class TimeApp(App): 
    def build(self): 
        return MainWidget() 
  
# Run the App 
TimeApp().run() 