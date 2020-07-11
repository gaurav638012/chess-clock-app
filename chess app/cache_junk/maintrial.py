from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '800')

class YourApp(App):
    def build(self):
        root_widget = BoxLayout(orientation='vertical')

        output_label = Label(size_hint_y=1)

        button_symbols = ('1', '2', '3', '+',
                          '4', '5', '6', '-',
                          '7', '8', '9', '.',
                          '0', '*', '/', '=')

        button_grid = GridLayout(cols=4, size_hint_y=2)
        for symbol in button_symbols:
            button_grid.add_widget(Button(text=symbol))

        clear_button = Button(text='clear', size_hint_y=None,
                              height=100)

        def print_button_text(instance):
            output_label.text += instance.text
        for button in button_grid.children[1:]:  # note use of the
                                             # `children` property
            button.bind(on_press=print_button_text)
        
        def resize_label_text(label, new_height):
            
            
            label.font_size = 0.5*label.height
        output_label.bind(height=resize_label_text)

        def evaluate_result(instance):
            try:
                output_label.text = str(eval(output_label.text))
            except SyntaxError:
                output_label.text = 'Python syntax error!'
        button_grid.children[0].bind(on_press=evaluate_result)

        def clear_label(instance):
            output_label.text = ''
        clear_button.bind(on_press=clear_label)

        root_widget.add_widget(output_label)
        root_widget.add_widget(button_grid)
        root_widget.add_widget(clear_button)

        return root_widget


YourApp().run()
    