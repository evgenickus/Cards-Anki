from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.properties import StringProperty, ColorProperty
from datetime import datetime, timedelta
import crud


class Menu(Screen):
  def screens_order(self):
    user_result = crud.get_user("default_user")
    last_action = user_result[3]
    action_time = datetime.fromisoformat(last_action)
    next_time = action_time + timedelta(minutes=2)
    can_next_round = datetime.now() > next_time
    if can_next_round:
      self.manager.current = "main"
    else:
      self.manager.current = "progress"

class Progress(Screen):
  pass

class MainWidget(Screen):
  user_db = crud.get_user("default_user")
  cards_db = crud.read_cards()
  step = 0
  round = 0

  round_cards = str()

  front = StringProperty("")
  back = StringProperty("")
  new = StringProperty("")
  inround = StringProperty("")
  studied = StringProperty("")
  picture_link = StringProperty("")



  def __init__(self, **kw):
    super(MainWidget, self).__init__(**kw)
    self.ids.main_box.remove_widget(self.ids.rating_box)
    self.init_users()
    self.init_cards()
    self.init_round_cards()
    self.front = self.round_cards[0][1]
    self.round = self.cards_db[1]
    self.step = self.cards_db[2]

  def init_users(self):
    if self.user_db == None:
      crud.create_default_user("default_user")
      self.user_db = crud.get_user("default_user")

  def init_cards(self):
    if self.cards_db == []:
      crud.create_default_cards()
      self.cards_db = crud.read_cards()

  def init_round_cards(self):
    self.round_cards = [i for i in self.cards_db[self.round * 11 + self.step : (self.round * 11 + self.step) + 11]]

  def style_back(self, back):
    return f"[color=008eff][u]{back[0].upper()}[/u][/color]{back[1]}[color=008eff][u]{back[2].upper()}[/u][/color]{back[3:]}"

  def find_word(self, id):
    card_db = crud.get_card(id)
    self.back = self.style_back(str(card_db[2]))
    self.picture_link = f"images/{card_db[3]}.jpg"

  def change_widget_open(self):
    self.ids.main_box.remove_widget(self.ids.open_button)
    self.ids.main_box.add_widget(self.ids.rating_box)
  
  def change_widget_rating(self):
    self.ids.main_box.remove_widget(self.ids.rating_box)
    self.ids.main_box.add_widget(self.ids.open_button)

  def open_card(self):
    self.find_word(self.round_cards[0][0])
    self.change_widget_open()

  def get_next_card(self):
    self.round_cards.remove(self.round_cards[0])
    self.front = self.round_cards[0][1]

  def rating(self, rating):
    self.picture_link = ""
    self.back = ""
    self.change_widget_rating()
    if rating == "easy":
      status = 1
    elif rating == "good":
      status = 2
    elif rating == "again":
      status = 3
    elif rating == "hard":
      status = 4
    crud.update_card_status(self.round_cards[0][0], status)
    self.get_next_card()



class CardsApp(App):
  main_color = ColorProperty([255/255, 122/255, 0, 1])
  def build(self):
    sm = ScreenManager(transition=FadeTransition())
    sm.add_widget(Menu(name="menu"))
    sm.add_widget(MainWidget(name="main"))
    sm.add_widget(Progress(name="progress"))
    return sm

if __name__ == "__main__":
  CardsApp().run()