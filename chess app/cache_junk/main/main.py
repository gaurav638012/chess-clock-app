import os,csv
import pandas as pd
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager,Screen
from KivyCalendar import DatePicker
from kivy.graphics import Color,Rectangle

class CustomDatePicker(DatePicker):
    def __init__(self,Calendar):
        super().__init__()
        self.calen = Calendar 

    def update_value(self, inst):
        """ Update textinput value on popup close """

        string_list = []
        for x in self.cal.active_date:
            string_list.append(str(x).zfill(2))
        self.text = "%s.%s.%s" % tuple(string_list)
        self.focus = False
        self.calen.ids.ti.text = self.text

class Calendar(BoxLayout):

    def show_calendar(self):
        datePicker = CustomDatePicker(self)
        datePicker.show_popup(1, .3)

def update(username,password):
    Data = pd.read_csv('Database.csv')
    for u in Data.Username:
        if(username==u):return False
    with open('Database.csv','a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([username,password])
    directory = username
    parent_dir = './'
    path = os.path.join(parent_dir,directory)
    os.mkdir(path)
    return True

def check(username,password):
    Data = pd.read_csv('Database.csv')
    for [u,p] in Data[['Username','Password']].to_numpy():
        if (u==username and p==password):
            return True
    return False

class NoteScreenWidget(Screen):
    def __init__(self,username,file_name):
        super().__init__()
        self.add_widget(NoteScreen(username,file_name))

class AddnewScreenWidget(Screen):
    def __init__(self,username):
        super().__init__()
        self.add_widget(AddnewScreen(username))
            
class DiaryScreenWidget(Screen):
    def __init__(self,username):
        super().__init__()
        self.add_widget(DiaryScreen(username))
        
class HomeScreenWidget(Screen):
    def __init__(self,username):
        super().__init__()
        self.add_widget(HomeScreen(username))
        
class SigninScreenWidget(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.add_widget(SigninScreen())
        
class LoginScreenWidget(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.add_widget(LoginScreen())
        
class NoteScreen(GridLayout):
    def __init__(self,username,file_name):
        super().__init__()
        self.username = username
        self.file_name = file_name
        self.file_title = file_name[11:]
        self.file_date = file_name[:10]
        file = open('./'+username+'/'+file_name+'.txt','r')
        
        self.body = file.read()
        
        self.cols = 2
        
        self.add_widget(Label(text='Title'))
        
        self.title = Label(text=self.file_title)
        self.add_widget(self.title)
        
        self.add_widget(Label(text='Body'))
        
        self.text = Label(text=self.body)
        self.add_widget(self.text)
        
        self.add_widget(Label(text='Date'))
        self.add_widget(Label(text=self.file_date))
        
        self.delete = Button(text='Delete')
        self.add_widget(self.delete)
        self.delete.bind(on_press=self.delete_pressed) 
        
        self.back = Button(text='Back')
        self.add_widget(self.back)
        self.back.bind(on_press=self.back_pressed) 
        
    def delete_pressed(self,instance):
        os.remove('./'+self.username+'/'+self.file_name+'.txt')
        Manager.switch_to(DiaryScreenWidget(self.username))
        
    def back_pressed(self,instance):
        Manager.switch_to(DiaryScreenWidget(self.username))
        
class AddnewScreen(GridLayout):
    def __init__(self,username):
        super().__init__()
        self.username = username
        self.cols = 2
        
        self.add_widget(Label(text='Title'))
        
        self.title = TextInput(multiline=False)
        self.add_widget(self.title)
        
        self.add_widget(Label(text='Body'))
        
        self.body = TextInput()
        self.add_widget(self.body)
        
        self.add_widget(Label(text='Date'))
        
        self.calendar = Calendar()
        self.add_widget(self.calendar)
        
        self.done = Button(text='Done')
        self.add_widget(self.done)
        self.done.bind(on_press=self.done_pressed)
        
        self.back = Button(text='Back')
        self.add_widget(self.back)
        self.back.bind(on_press=self.back_pressed)
        
    def done_pressed(self,instance):
        self.date = self.calendar.ids.ti.text
        save_path = './'+self.username+'/'
        name = os.path.join(save_path,self.date+'_'+self.title.text+'.txt')
        for n in os.listdir(save_path):
            if(self.date+'_'+self.title.text+'.txt'==n): 
                self.title.text=''
                return False
        file = open(name,'w')
        file.write(self.body.text)
        file.close()
        Manager.switch_to(DiaryScreenWidget(self.username))
        
    def back_pressed(self,instance):
        Manager.switch_to(DiaryScreenWidget(self.username))
        
class DiaryScreen(GridLayout):
    def __init__(self,username):
        super().__init__()
        self.username = username
        self.cols = 1
        
        self.list = []
        
        for n in os.listdir('./'+self.username+'/'):
            if(n.endswith('.txt')):
                self.list.append(Button(text=n[:-4]))
                self.add_widget(self.list[-1])
                self.list[-1].bind(on_press=lambda x:self.note_pressed(n[:-4]))
        
        self.add = Button(text='Add a new note')
        self.add_widget(self.add)
        self.add.bind(on_press=self.add_pressed)
        
        self.back = Button(text='Back to Home')
        self.add_widget(self.back)
        self.back.bind(on_press=self.back_pressed)
        
    def back_pressed(self,instance):
        Manager.switch_to(HomeScreenWidget(self.username))
        
    def add_pressed(self,instance):
        Manager.switch_to(AddnewScreenWidget(self.username))
        
    def note_pressed(self,title):
        Manager.switch_to(NoteScreenWidget(self.username,title))
        
class HomeScreen(GridLayout):
    def __init__(self,username):
        super().__init__()
        self.username = username
        self.cols = 1
        self.add_widget(Label(text='Home Screen\nWelcome '+username))
        
        self.diary = Button(text='Open Notes')
        self.add_widget(self.diary)
        self.diary.bind(on_press=self.diary_pressed)
        
        self.logout = Button(text='Log Out')
        self.add_widget(self.logout)
        self.logout.bind(on_press=self.logout_pressed)
        
    def logout_pressed(self,instance):
        Manager.switch_to(LoginScreenWidget())
        
    def diary_pressed(self,instance):
        Manager.switch_to(DiaryScreenWidget(self.username))
        
class SigninScreen(GridLayout):
    def __init__(self):
        super().__init__()
        self.cols = 2
        
        self.add_widget(Label(text='Username'))
        
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        
        self.add_widget(Label(text='Password'))
        
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        
        self.signin = Button(text='Sign in')
        self.add_widget(self.signin)
        self.signin.bind(on_press=self.signin_pressed)
        
        self.back = Button(text='Back')
        self.add_widget(self.back)
        self.back.bind(on_press=self.back_pressed)
        
    def signin_pressed(self,instance):
        if(update(self.username.text,self.password.text)):
            Manager.switch_to(HomeScreenWidget(self.username.text))
        else:
            self.username.text=""
            self.password.text="" 
    
    def back_pressed(self,instance):
        Manager.switch_to(LoginScreenWidget())

class LoginScreen(GridLayout):
    def __init__(self):
        super().__init__()
        self.cols = 2
        
        self.label1 = Label(text='User Name')
        self.add_widget(self.label1)
        
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        
        self.add_widget(Label(text='Password'))
        
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        
        self.signin = Button(text='Sign in')
        self.add_widget(self.signin)
        #self.signin.bind(on_press=self.signin_pressed)
        
        self.login = Button(text='Login')
        self.add_widget(self.login)
        #self.login.bind(on_press=self.login_pressed)
        
    def login_pressed(self,instance):
        if(check(self.username.text,self.password.text)):
            Manager.switch_to(HomeScreenWidget(self.username.text))
        else:
            self.username.text=""
            self.password.text=""
        
    def signin_pressed(self,instance):
        Manager.switch_to(SigninScreenWidget())

Manager = ScreenManager()
Manager.add_widget(LoginScreenWidget())       

class MyApp(App):
    def build(self):
        return LoginScreen()
    
if __name__ == '__main__':
    MyApp().run()