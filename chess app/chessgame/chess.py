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
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
import csv
import pandas as pd
class choose_layout(BoxLayout):
    
    def __init__(self,colors):
        super().__init__()
        self.time={'hour':'0','minute':'5','second':'00'}
        self.hour= time_layout('hour',24,colors)
        self.minute= time_layout('minute',60,colors)
        self.second= time_layout('second',60,colors)
        
        self.add_widget(self.hour)
        self.add_widget(self.minute)
        self.add_widget(self.second)
      
    def set_time_dict(self,timer):
        timer['hour']=self.hour.label1.text
        timer['minute']=self.minute.label1.text
        timer['second']=self.second.label1.text

class time_layout(BoxLayout):
    def __init__(self,strin,no,colors):
        super().__init__()
        self.orientation="vertical"
        """self.scrlv=ScrollView(size_hint=(0.8,0.8))
        temp=GridLayout(cols=1, size_hint_y=None)
        temp.bind(minimum_height=temp.setter('height'))"""
        self.s=Slider(value=0,min=0,max=no-1,step=1)
        """
        for i in range(0, no):
            btn = Label(text=str(i), size_hint_y=None, size_hint_x=0.2,height=10, valign='middle',halign='center', font_size=5)
            btn.text_size = (btn.size)
            temp.add_widget(btn)
        self.scrlv.add_widget(temp)"""
        label=Label(text=strin,color=colors)
        #self.label1=Label(text=str(int((1-self.scrlv.scroll_y)*no)))
        self.label1=Label(text=str(int(self.s.value)),color=colors)
        """def corelate(instance,value):
            self.label1.text=str(int((1-self.scrlv.scroll_y)*no))"""
        def corelate(instance,value):
            self.label1.text=str(int(self.s.value))
        #self.scrlv.bind(scroll_y=corelate)
        self.s.bind(value=corelate)
        
        self.add_widget(label)
        self.add_widget(self.label1)
        self.add_widget(self.s)
        #self.add_widget(self.scrlv)
class add_time_button(Button):
    
    def __init__(self,lister):
        super().__init__()
        self.size_hint=(0.3,0.2)
        self.text=lister[0]+" "+lister[1]+"\n"+lister[2]+" "+lister[3]

def string_dissecct(strings):
    c1=strings.find(" ")
    c2=strings.find("\n")
    c3=strings.find(" ",c1+1)
    return [strings[:c1],strings[c1+1:c2],strings[c2+1:c3],strings[c3+1:]]
   
         
def string_to_dict(strings):
    dicts={}
    count=strings.count(":")
    if(count==2):
        c1=strings.find(":")
        dicts['hour']=strings[0:c1]
        c2=strings.find(":",c1+1)
        dicts['minute']=strings[c1+1:c2]
        dicts['second']=strings[c2+1:]
    else:
        c1=strings.find(":")
        dicts['hour']='0'
        dicts['minute']=strings[:c1]
        dicts['second']=strings[c1+1:]
    return dicts

class FirstScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.a=BoxLayout(orientation="vertical")
        self.list_of_buttons=[]
        self.no_of_buttons=0

        self.set_add_time_button()
        
    def set_tim(self,instance):
            print(type(instance.text))
            lister=string_dissecct(instance.text)
            white_time1=string_to_dict(lister[0])
            black_time1=string_to_dict(lister[1])
            white_increment_time1=string_to_dict(lister[2])
            black_increment_time1=string_to_dict(lister[3])
            
            def do_u_want_to_set():
                are_u_sure_layout=BoxLayout()
                are_u_sure=Popup(title='do u want these values',content=are_u_sure_layout,size_hint=(0.4,0.4),auto_dismiss=False)
                yes_button=Button(text="yes",size_hint=(0.5,0.4))
                no_button=Button(text="no",size_hint=(0.5,0.4))
                yes_button.bind(on_press=lambda x:self.set_timings(white_time1,black_time1,white_increment_time1,black_increment_time1))
                yes_button.bind(on_release=lambda x:are_u_sure.dismiss())
                no_button.bind(on_press=lambda x:are_u_sure.dismiss())
                are_u_sure_layout.add_widget(yes_button)
                are_u_sure_layout.add_widget(no_button)
                are_u_sure.open()
            do_u_want_to_set()
            


    def set_add_time_button(self):
        x=pd.read_csv("created_games.csv")
    
        for ind in x.index:
            
            self.list_of_buttons.append(add_time_button(x.loc[ind]))
            #print(temp_string)
            #c=self.list_of_buttons[ind]
            
            self.list_of_buttons[ind].bind(on_press=self.set_tim)
            self.no_of_buttons+=1
            #self.a.add_widget(c,index=ind)
            #p.bind(on_press=lambda x:self.set_white_black())
        temp=9
        for w in reversed(self.list_of_buttons):
            if(temp>=0):
                self.a.add_widget(w)
                temp-=1
            
        self.add_widget(self.a)
               
    def add_time(self,lister):
        with open("created_games.csv","a") as file:
            csvwriter=csv.writer(file)
            csvwriter.writerow(lister)
            #temp=add_time_button(lister)
            #print(lister)
            #temp.bind(on_press=lambda x:self.set_tim(lister))
            self.list_of_buttons.append(add_time_button(lister)) 
            self.no_of_buttons+=1
            self.list_of_buttons[self.no_of_buttons-1].bind(on_press=self.set_tim)
            
            if(self.no_of_buttons>10):
                self.a.remove_widget(self.list_of_buttons[self.no_of_buttons-11])
            self.a.add_widget(self.list_of_buttons[self.no_of_buttons-1],index=9)
    
    def create_new_popup(self):
        pop_layout=BoxLayout(orientation='vertical')
        popup=Popup(title='create the game',content=pop_layout,size_hint=(0.8,0.8),auto_dismiss=False)

        orient_white_black=BoxLayout()
        white_layout=choose_layout([1,1,1,1])
        black_layout=choose_layout([0,0,0,1])
        text_white_black= BoxLayout(size_hint=(1,0.1))
        label_white=Label(text="White",size_hint=(0.3,0.1),pos_hint={'top':1,'left':0})
        label_black=Label(text="Black",color=[0,0,0,1],size_hint=(0.3,0.1),pos_hint={'top':1,'right':1})
        text_white_black.add_widget(label_white)
        text_white_black.add_widget(label_black)
        orient_white_black.add_widget(white_layout)
        orient_white_black.add_widget(black_layout)

        increment_label=Label(text="Increment Time",color=[1,0,0,1])
        
        orient_white_black1=BoxLayout()
        white_layout1=choose_layout([1,1,1,1])
        black_layout1=choose_layout([0,0,0,1])
        orient_white_black1.add_widget(white_layout1)
        orient_white_black1.add_widget(black_layout1)

        button_layout=BoxLayout()
        button=Button(text='set it',size_hint=(1,0.3))
        button1=Button(text='leave',size_hint=(1,0.3))
        button1.bind(on_press=lambda x:u_want_to_f())
        button.bind(on_press=lambda x:are_u_sure_f())
        button_layout.add_widget(button)
        button_layout.add_widget(button1)

        def are_u_sure_f():
            are_u_sure_layout=BoxLayout()
            are_u_sure=Popup(title='do u want these values',content=are_u_sure_layout,size_hint=(0.4,0.4),auto_dismiss=False)
            yes_button=Button(text="yes",size_hint=(0.5,0.4))
            no_button=Button(text="no",size_hint=(0.5,0.4))

            def out(instance):
                are_u_sure.dismiss()
                popup.dismiss()

            yes_button.bind(on_press=lambda x:set_white_black())
            yes_button.bind(on_release=out)
            no_button.bind(on_press=lambda x:are_u_sure.dismiss())
            are_u_sure_layout.add_widget(yes_button)
            are_u_sure_layout.add_widget(no_button)
            
            are_u_sure.open()
        
        def u_want_to_f():
            do_u_want_layout=BoxLayout()
            do_u_want=Popup(title='do u want to leave',content=do_u_want_layout,size_hint=(0.4,0.4),auto_dismiss=False)
            yes_button=Button(text="yes",size_hint=(0.5,0.4))
            no_button=Button(text="no",size_hint=(0.5,0.4))
            
            def out(instance):
                do_u_want.dismiss()
                popup.dismiss()

            yes_button.bind(on_press=out)
            no_button.bind(on_press=lambda x:do_u_want.dismiss())
            do_u_want_layout.add_widget(yes_button)
            do_u_want_layout.add_widget(no_button)
            
            do_u_want.open()
            
        def set_white_black():
            white_layout.set_time_dict(white_layout.time)
            black_layout.set_time_dict(black_layout.time)
            white_layout1.set_time_dict(white_layout1.time)
            black_layout1.set_time_dict(black_layout1.time)
            self.add_time([format_time(white_layout.time),format_time(black_layout.time),format_time(white_layout1.time),format_time(black_layout1.time)])
            self.set_timings(white_layout.time,black_layout.time,white_layout1.time,black_layout1.time)
        
        pop_layout.add_widget(text_white_black)
        pop_layout.add_widget(orient_white_black)
        pop_layout.add_widget(increment_label)
        pop_layout.add_widget(orient_white_black1)
        pop_layout.add_widget(button_layout)
        popup.open()       

    def set_timings(self,dict1,dict2,incre_dict1,incre_dict2):
        p=self.manager.get_screen('second')
    
        p.new_value_setter(dict1,dict2)
        p.increment_setter(incre_dict1,incre_dict2)
    
class MyScreenManager(ScreenManager):
    pass

class SecondScreen(Screen):
                                                   #flags=-1 represents game not started and only black can press since white starts
    pause_flag=1
    white_time_init=kv.DictProperty({'hour':'0','minute':'5','second':'00'})  # dictionary to hold time of white and black
    black_time_init=kv.DictProperty({'hour':'0','minute':'5','second':'00'})
    increment_white_time=kv.DictProperty({'hour':'0','minute':'0','second':'02'})
    increment_black_time=kv.DictProperty({'hour':'0','minute':'0','second':'02'})
    white_time=kv.DictProperty({'hour':'0','minute':'5','second':'00'})  # dictionary to hold time of white and black
    black_time=kv.DictProperty({'hour':'0','minute':'5','second':'00'})
    white_string=kv.StringProperty('5:00')
    black_string=kv.StringProperty("5:00")                  #strings which contain display of white and black time
    flags=-1
    def __init__(self, **kw):
        super().__init__(**kw)
        df=pd.read_csv("helo.csv")
        #elf.pause_flag=int(df.loc[0]['pause_flag'])    # fields=['flags','pause_flag','white_string','black_string','increment_white','increment_black']
        self.white_time=string_to_dict(df.loc[0]['white_string'])
        self.black_time=string_to_dict(df.loc[0]['black_string'])
        self.white_string=df.loc[0]['white_string']
        self.black_string=df.loc[0]['black_string']
        self.white_time_init=string_to_dict(df.loc[0]['init_white'])
        self.black_time_init=string_to_dict(df.loc[0]['init_black'])
        self.increment_white_time=string_to_dict(df.loc[0]['increment_white'])
        self.increment_black_time_=string_to_dict(df.loc[0]['increment_black'])
        self.flags=df.loc[0]['flags']
        
    def value_time(self,dict):
       return int(dict['second'])+int(dict['minute'])*60+int(dict['hour'])*3600
    def increment_setter(self,dict1,dict2):
        self.increment_white_time=dict1
        self.increment_black_time=dict2
        
   

    def new_value_setter(self,dict1,dict2):
        self.flags=-1
        self.pause_flag=0
        self.white_time_init=dict1
        self.black_time_init=dict2
        self.white_time=dict1
        self.black_time=dict2
        self.white_string=format_time(self.white_time)
        self.black_string=format_time(self.black_time)
        white=self.ids['white']
        black=self.ids['black']
        white.background_color=[0,1,1,1]
        black.background_color=[0,1,1,1]

    def refresher(self):  
        self.exit_pauser()  
        pop_layout=BoxLayout()
        popup=Popup(title="Are u sure u want to refresh",content=pop_layout)       
        pop_label=Label(text="Refresh will make \n current time lost",font_size=50,color=[1,0.7,0.435,1],halign='right',valign='middle') 
        q=BoxLayout(orientation="horizontal")
        yes_button=Button(text="yes",size_hint=(0.6,0.2))
        no_button=Button(text="no",size_hint=(0.6,0.2)) 
        def out(instance):          
            Clock.unschedule(self.decrease_time_default_white)
            Clock.unschedule(self.decrease_time_default_black)
            self.flags=-1
            self.pause_flag=1
            labels=self.ids['pause_button']                            
            labels.text="pause"
            self.white_time=self.white_time_init
            self.black_time=self.black_time_init
            self.white_string=format_time(self.white_time)
            self.black_string=format_time(self.black_time)
            white=self.ids['white']
            black=self.ids['black']
            white.background_color=[0,1,1,1]
            black.background_color=[0,1,1,1]
            popup.dismiss()

        yes_button.bind(on_press=out)
        no_button.bind(on_press=lambda x:popup.dismiss())
        pop_layout.add_widget(pop_label)
        q.add_widget(yes_button)
        q.add_widget(no_button)
        pop_layout.add_widget(q)
        popup.open()
     
    def exit_pauser(self):
        if(self.pause_flag==1):                                      # if flag 1 then clock is ticking
            if(self.flags==1):
                Clock.unschedule(self.decrease_time_default_white)            # unschedule white  flags=1 represents white time is going 
            elif(self.flags==0):                                                # unschedule black  flags=1 represents black time is going 
                Clock.unschedule(self.decrease_time_default_black)
            labels=self.ids['pause_button']                            
            labels.text="resume"                                          #interchange between resume and pause
            self.pause_flag=0

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
        if(self.value_time(self.black_time)==0):
            white=self.ids['black']
            white.background_color=[1,0,0,1]
            self.flags=-2
            return      
        self.black_time['second']=str(int(self.black_time['second'])-1)
        if(int(self.black_time['second'])<0):
            self.black_time['minute']=str(int(self.black_time['minute'])-1)
            self.black_time['second']=str(int(self.black_time['second'])+60)                   #decrease the time in black by 1 sec
            
        if(int(self.black_time['minute'])<0):
            self.black_time['hour']=str(int(self.black_time['hour'])-1)
            self.black_time['minute']=str(int(self.black_time['minute'])+60)
        self.black_string=format_time(self.black_time) # update in the string
    
    def incrementer_black(self):
        self.black_time['second']=str(int(self.black_time['second'])+int(self.increment_black_time['second']))
        self.black_time['minute']=str(int(self.black_time['minute'])+int(self.increment_black_time['minute']))
        self.black_time['hour']=str(int(self.black_time['hour'])+int(self.increment_black_time['hour']))
        seconder=int(self.black_time['second'])%60
        minuter=int(int(self.black_time['second'])/60)+int(self.black_time['minute'])
        hourer=int(self.black_time['hour'])+int(minuter/60)
        minuter=minuter%60
        hourer=hourer%24
        self.black_time['hour']=str(hourer)
        self.black_time['minute']=str(minuter)
        self.black_time['second']=str(seconder)
        self.black_string=format_time(self.black_time)

    def incrementer_white(self):
        self.white_time['second']=str(int(self.white_time['second'])+int(self.increment_white_time['second']))
        self.white_time['minute']=str(int(self.white_time['minute'])+int(self.increment_white_time['minute']))
        self.white_time['hour']=str(int(self.white_time['hour'])+int(self.increment_white_time['hour']))
        seconder=int(self.white_time['second'])%60
        minuter=int(int(self.white_time['second'])/60)+int(self.white_time['minute'])
        hourer=int(self.white_time['hour'])+int(minuter/60)
        minuter=minuter%60
        hourer=hourer%24
        self.white_time['hour']=str(hourer)
        self.white_time['minute']=str(minuter)
        self.white_time['second']=str(seconder)
        self.white_string=format_time(self.white_time)


    def decrease_time_default_white(self,dt):
        if(self.value_time(self.white_time)==0):
            white=self.ids['white']
            white.background_color=[1,0,0,1]
            self.flags=2
            return
        self.white_time['second']=str(int(self.white_time['second'])-1)
        if(int(self.white_time['second'])<0):
            self.white_time['minute']=str(int(self.white_time['minute'])-1)
            self.white_time['second']=str(int(self.white_time['second'])+60)                #decrease the time in black by 1 sec
            
        if(int(self.white_time['minute'])<0):
            self.white_time['hour']=str(int(self.white_time['hour'])-1)
            self.white_time['minute']=str(int(self.white_time['minute'])+60)

        self.white_string=format_time(self.white_time)
        

            
    def click_setter_black(self ):
        white=self.ids['white']                #if clicked on black
        black=self.ids['black']           
        if(self.flags ==-1 and self.value_time(self.black_time)>0 and self.pause_flag==1):          # beginning of the game
            white.background_color=[1,1,1,1]  #running color
            black.background_color=[0,1,0,1]  #dormant color        
            self.flags=1                                                     
            Clock.schedule_interval(self.decrease_time_default_white,1)
            print(self.white_string)
        elif(self.flags ==-1 and self.value_time(self.black_time)==0 and self.pause_flag==1):
            black.background_color=[1,0,0,1] 
            white.background_color=[1,0,0,1] 
            self.flags=-2
            Clock.unschedule(self.decrease_time_default_black)
            Clock.unschedule(self.decrease_time_default_white)
        elif(self.flags==0 and self.value_time(self.black_time)>0 and self.pause_flag==1):               # if black presses and its his turn
            white.background_color=[1,1,1,1]
            black.background_color=[0,1,0,1]  
            self.flags=1  
            self.incrementer_black() 
            Clock.unschedule(self.decrease_time_default_black)     
             
            Clock.schedule_interval(self.decrease_time_default_white,1)
        elif(self.flags==0 and self.value_time(self.black_time)==0 and self.pause_flag==1):
            white.background_color=[0,1,1,1]
            black.background_color=[1,0,0,1] 
            self.flags=-2
            Clock.unschedule(self.decrease_time_default_black)
            Clock.unschedule(self.decrease_time_default_white)
    
    def click_setter_white(self):        # similar to black
        white=self.ids['white']
        black=self.ids['black']     
        if(self.flags==1 and self.value_time(self.white_time)>0 and self.pause_flag==1):
            white.background_color=[0,1,0,1]
            black.background_color=[1,1,1,1]  
            self.flags=0
            self.incrementer_white()
            Clock.unschedule(self.decrease_time_default_white)
            Clock.schedule_interval(self.decrease_time_default_black,1)
        elif(self.flags==1 and self.value_time(self.white_time)==0 and self.pause_flag==1):
            white.background_color=[1,0,0,1]
            black.background_color=[0,1,1,1]
            self.flags=2
            Clock.unschedule(self.decrease_time_default_black)
            Clock.unschedule(self.decrease_time_default_white)

def format_time(dict):
    if(int(dict['second'])<10):
        dict['second']='0'+str(int(dict['second']))
    
    if(int(dict['hour'])==0):
         return dict['minute']+':'+dict['second']
    else:
        if(int(dict['minute'])<10):
            dict['minute']='0'+str(int(dict['minute']))
        return dict['hour']+':'+dict['minute']+':'+dict['second']


root_widget=Builder.load_string('''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
MyScreenManager:
    transition: FadeTransition()
    SecondScreen:
    FirstScreen:

<SecondScreen>:
    name:"second"
    FloatLayout:
        Button:
            id: refresh_button
            font_size : 20
            size_hint: 0.1,0.1
            pos_hint: {'center_x':0.5,'top':1}
            text : "refresh"
            background_color : [1,1,0,1]
            on_press:root.refresher()
        Button:
            id: exit_button
            font_size : 20
            size_hint: 0.1,0.1
            pos_hint : {'center_x':0.5,'bottom':0}
            text : "exit"
            background_color : [1,1,0,1]
            on_press:root.exit_pauser()
            on_release:app.root.current='First'
        Button:
            id: pause_button
            font_size : 20
            size_hint: 0.1,0.1
            pos_hint : {'center_x':0.5,'center_y':0.5}
            text : "pause"
            background_color : [1,1,0,1]
            on_release:root.pauser()
        Button:
                            
            id:white
            size_hint:0.45,0.9
            background_color : [0,1,1,1]
            on_press: root.click_setter_white()
            text:root.white_string
            font_size:100
        Label:
            text:'white'
            font_size:20
            size_hint:0.1,0.1
            pos_hint:{'left':0,'top':1}   
        Button:
            id:black
            size_hint:0.45,0.9
            pos_hint: {'right':1,'top':0.9}
            background_color : [0,1,1,1]
            on_press:root.click_setter_black()
            text:root.black_string
            font_size:100
        Label:
            text:'black'
            font_size:20
            size_hint:0.1,0.1
            pos_hint:{'right':1,'top':1}  
<FirstScreen>:
    name:'First'
    FloatLayout:
        
        Button:
            size_hint:0.13,0.13
            pos_hint:{'top':1,'right':1}
            text:'move to timer'
            font_size:13
            on_press:app.root.current='second'
        Button:
            size_hint:0.15,0.15
            pos_hint:{'bottom':0,'right':1}
            text:'create new game'
            on_press:root.create_new_popup()

''')
class homewidget(FloatLayout):
    pass
class chessApp(App):
    def build(self):   
        return root_widget
    def on_stop(self):
        p=root_widget.get_screen('second')
        #p.pause_flag=1
        fields=['flags','pause_flag','white_string','black_string','init_white','init_black','increment_white','increment_black']
        with open("helo.csv",'w') as file:
            csvwriter=csv.writer(file)
            csvwriter.writerow(fields)
            c=p.flags
            if(p.flags==1):
                c=0
            elif(p.flags==0):
                c=1
            lis=[c,1,p.white_string,p.black_string,format_time(p.white_time_init),format_time(p.black_time_init),
            format_time(p.increment_white_time),format_time(p.increment_black_time)]
            print(lis)
            csvwriter.writerow(lis)

chessApp().run()