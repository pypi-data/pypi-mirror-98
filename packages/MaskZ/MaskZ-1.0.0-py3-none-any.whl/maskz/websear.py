import random # It will take time I guess
import webbrowser as wb
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

wb.register(
    'cr',
    None,
    wb.BackgroundBrowser('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe') # Got my chrome path

)

class Lay(GridLayout): # Grid not Gird
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 2
        self.cols = 1
        Button.background_color = 1.2, 0.34, 1, 0.8

        self.inp = TextInput(multiline=True)
        self.add_widget(self.inp)

        self.src = Button(text="Search The Web", font_size=45)
        self.src.bind(on_press=self.pressed)
        self.add_widget(self.src)
        # self.add_widget(Label(text="test for Grid Layout"))  # I am gonna make this short\

    def pressed(self, instance):
        wb.get('cr').open(self.inp.text)

    # Now  I will test my own website I made yesterday
    # Happy new Year





class WebCrawler(App):
    def build(self):
        a = Lay()
        return a



WebCrawler().run()
