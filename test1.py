from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class MainWidget(BoxLayout):
  a = 0
 
  def __init__(self, **kwargs):
    super(MainWidget, self).__init__(**kwargs)

  def print_a(self):
    self.a += 1 
    print(self.a)
   

class StartApp(App):

  def build(self):
    return MainWidget()
  


if __name__ == "__main__":
  StartApp().run()