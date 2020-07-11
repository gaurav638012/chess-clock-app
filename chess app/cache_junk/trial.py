from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen


class MyScreenManager(ScreenManager):
    pass


class TestScreen(Screen):
    pass





class Scroller(ScrollView):
    def __init__(self):
        ScrollView.__init__(self)
        layout = GridLayout(cols=1, size_hint=(1, None))
        self.add_widget(layout)
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(20):
            layout.add_widget(Field('Test field {}'.format(i), i%2 is 0))


class Field(GridLayout):
    def __init__(self, name, bg):
        assert isinstance(name, str)
        assert isinstance(bg, bool)
        self.bg = bg
        GridLayout.__init__(self,
                            rows = 1,
                            padding = 10,
                            size = (0, 60),
                            size_hint = (1, None))
        self.add_widget(Label(text = name))
        self.add_widget(Button(text = 'Test',
                               size = (200, 0),
                               size_hint = (None, 1)))
        self.bind(pos = self.change_background)
        self.bind(size = self.change_background)

    def change_background(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(.4, .4, .4, mode='rgb')
            Rectangle(size=self.size, pos=self.pos)

class Main(App):
    def build(self):
        layout = FloatLayout()
        layout.add_widget(Scroller())
        testscreen = TestScreen(name='TestScreen')
        testscreen.add_widget(layout)
        root = MyScreenManager()
        root.add_widget(screen=testscreen)
        return root 

Main().run()
