from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.properties import DictProperty

class Main(Screen):
    pass

class MyApp(MDApp): 
    data = DictProperty()
    sm = ScreenManager()
    def build(self):
        self.title = 'MyApp'
        self.sm.add_widget(Main(name='main'))
        return self.sm
   
if __name__ == "__main__":
    MyApp().run()
