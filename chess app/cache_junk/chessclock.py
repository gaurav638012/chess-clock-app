from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.stacklayout import StackLayout
import kivy.properties as kv
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
class FirstScreen(Screen):
    pass

class SecondScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass

class mainwidget(FloatLayout):
                                                    #flags=-1 represents game not started and only black can press since white starts
    pause_flag=1
    white_time=kv.DictProperty({'hour':'0','minute':'5','second':'0'})  # dictionary to hold time of white and black
    black_time=kv.DictProperty({'hour':'0','minute':'5','second':'0'})
    white_string=kv.StringProperty('0:5:0')
    black_string=kv.StringProperty("0:5:0")                  #strings which contain display of white and black time

    def __init__(self):
        super(mainwidget, self).__init__() 
        self.flags=-1
    def refresher(self):                     
        Clock.unschedule(self.decrease_time_default_white)
        Clock.unschedule(self.decrease_time_default_black)
        self.flags=-1
        self.white_time={'hour':'0','minute':'5','second':'0'}
        self.black_time={'hour':'0','minute':'5','second':'0'}
        self.white_string='0:5:0'                                     #used to set times to initial state
        self.black_string="0:5:0"
    
    def pauser(self):                                               # used to pause the clock
        if(self.pause_flag==1):                                      # if flag 1 then clock is ticking
            if(self.flags==1):
                Clock.unschedule(self.decrease_time_default_white)            # unschedule white  flags=1 represents white time is going 
            elif(self.flags==0):                                                # unschedule black  flags=1 represents black time is going 
                Clock.unschedule(self.decrease_time_default_black)
            labels=self.ids['pause_button']                            
            labels.text="resume"                                          #interchange between resume and pause
            self.pause_flag=0
        elif(self.pause_flag==0):                                            # if flag=0 clock is paused either side it remains constant
            if(self.flags==1):                                             
                Clock.schedule_interval(self.decrease_time_default_white,1)        # resume time if move belongs to white
            elif(self.flags==0):                                                   
                Clock.schedule_interval(self.decrease_time_default_black,1)
            labels=self.ids['pause_button']
            labels.text="pause"                                         #interchange the name 
            self.pause_flag=1

    def decrease_time_default_black(self,dt):
              
        self.black_time['second']=str(int(self.black_time['second'])-1)
        if(int(self.black_time['second'])<0):
            self.black_time['minute']=str(int(self.black_time['minute'])-1)
            self.black_time['second']=str(int(self.black_time['second'])+60)                   #decrease the time in black by 1 sec
            
        if(int(self.black_time['minute'])<0):
            self.black_time['hour']=str(int(self.black_time['hour'])-1)
            self.black_time['minute']=str(int(self.black_time['minute'])+60)
        self.black_string=self.black_time['hour']+':'+self.black_time['minute']+':'+self.black_time['second'] # update in the string

    def decrease_time_default_white(self,dt):
        self.white_time['second']=str(int(self.white_time['second'])-1)
        if(int(self.white_time['second'])<0):
            self.white_time['minute']=str(int(self.white_time['minute'])-1)
            self.white_time['second']=str(int(self.white_time['second'])+60)                #decrease the time in black by 1 sec
            
        if(int(self.white_time['minute'])<0):
            self.white_time['hour']=str(int(self.white_time['hour'])-1)
            self.white_time['hour']=str(int(self.white_time['hour'])+60)
        self.white_string=self.white_time['hour']+':'+self.white_time['minute']+':'+self.white_time['second']
            
    def click_setter_black(self):
        white=self.ids['white']                #if clicked on black
        black=self.ids['black']           
        if(self.flags ==-1):          # beginning of the game
            white.background_color=[1,1,1,1]  #running color
            black.background_color=[0,1,0,1]  #dormant color        
            self.flags=1                                                     
            Clock.schedule_interval(self.decrease_time_default_white,1)
            print(self.white_string)
        elif(self.flags==0):               # if black presses and its his turn
            white.background_color=[1,1,1,1]
            black.background_color=[0,1,0,1]  
            self.flags=1  
            Clock.unschedule(self.decrease_time_default_black)               
            Clock.schedule_interval(self.decrease_time_default_white,1)
    
    def click_setter_white(self):        # similar to black
        white=self.ids['white']
        black=self.ids['black']     
        if(self.flags==1):
            white.background_color=[0,1,0,1]
            black.background_color=[1,1,1,1]  
            self.flags=0
            Clock.unschedule(self.decrease_time_default_white)
            Clock.schedule_interval(self.decrease_time_default_black,1)
class homewidget(FloatLayout):
    pass
class ChessClockApp(App):
    def build(self):   
        return mainwidget()

ChessClockApp().run()