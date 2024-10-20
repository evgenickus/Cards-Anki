from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.properties import StringProperty, ColorProperty
from datetime import datetime, timedelta
import crud


class Menu(Screen):
  current_user = "default_user"
  def screens_order(self):
    user_result = crud.get_user(self.current_user)
    last_action = user_result[3]
    action_time = datetime.fromisoformat(last_action)
    next_time = action_time + timedelta(minutes=1)
    can_next_round = datetime.now() > next_time
    if can_next_round:
      self.manager.current = "main"
    else:
      self.manager.current = "progress"

class Progress(Screen):
  pass

class MainWidget(Screen):
  current_user = "default_user"
  user_db = crud.get_user(current_user)
  cards_db = crud.read_cards()
  step = 0
  round = 0

  current_card = list()
  new_cards = list()
  inround_cards = list()
  studied_cards = list()

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
    self.round = self.user_db[1]
    self.step = self.user_db[2]
    self.init_new_cards()
    self.init_other_cards()
    self.init_count_labels()
    self.init_underline()
    self.init_current_card()

  def init_users(self):
    if self.user_db == None:
      crud.create_user(self.current_user)
      self.user_db = crud.get_user(self.current_user)

  def init_cards(self):
    if self.cards_db == []:
      crud.create_default_cards()
      self.cards_db = crud.read_cards()

  def init_new_cards(self):
    self.new_cards = [
      i for i in self.cards_db[self.round * 11 + self.step : (self.round * 11 + self.step) + 11 - self.step]
    ]
  
  def init_other_cards(self):
    for i in self.cards_db:
      if i[4] in [1, 2]:
        self.studied_cards.append(i)
      elif i[4] in [3, 4]:
        self.inround_cards.append(i)
  
  def init_count_labels(self):
    self.new = str(len(self.new_cards))
    self.inround = str(len(self.inround_cards))
    self.studied = str(len(self.studied_cards))


  def init_underline(self):
    if int(self.new) > 0:
      self.ids.new.underline = True
      self.ids.inround.underline = False
    elif int(self.new) == 0:
      self.ids.new.underline = False
      self.ids.inround.underline = True

  def init_current_card(self):
    if len(self.new_cards) > 0:
      self.current_card = self.new_cards[0]
      self.front = self.current_card[1]
    elif len(self.new_cards) == 0 and len(self.inround_cards) > 0:
      self.current_card = self.inround_cards[0]
      self.front = self.current_card[1]

  def stop_round(self):
    current_time = datetime.now()
    crud.update_round_time(self.current_user, current_time)
    self.manager.current = "progress"
    self.init_new_cards()
    self.init_current_card()

  def get_next_card(self):
    if len(self.new_cards) > 0:
      self.count_step()
      self.new_cards.remove(self.current_card)
      if len(self.new_cards) != 0:
        self.current_card = self.new_cards[0]
        self.front = self.current_card[1]
      elif len(self.new_cards) == 0 and len(self.inround_cards) > 0:
        self.current_card = self.inround_cards[0]
        self.front = self.current_card[1]
      else:
        self.stop_round()
    elif len(self.new_cards) == 0 and len(self.inround_cards) > 0:
      self.inround_cards.remove(self.current_card)
      if len(self.inround_cards) != 0:
        self.current_card = self.inround_cards[0]
        self.front = self.current_card[1]
      else:
        self.stop_round()
    else:
      self.stop_round()

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
    self.find_word(self.current_card[0])
    self.change_widget_open()

  def count_step(self):
    self.step += 1
    if self.step == 11:
      self.step = 0
      self.round += 1

  def rating(self, rating):
    self.picture_link = ""
    self.back = ""
    self.change_widget_rating()
    if rating == "easy":
      self.studied_cards.append(self.current_card)
      status = 1
    elif rating == "good":
      self.studied_cards.append(self.current_card)
      status = 2
    elif rating == "again":
      self.inround_cards.append(self.current_card)
      status = 3
    elif rating == "hard":
      self.inround_cards.append(self.current_card)
      status = 4
    crud.update_card_status(self.current_card[0], status)
    self.get_next_card()
    crud.update_step(self.round, self.step, self.current_user)
    self.init_count_labels()
    self.init_underline()


class CardsApp(App):
  main_color = ColorProperty([255/255, 122/255, 0, 1])
  def build(self):
    sm = ScreenManager(transition=NoTransition())
    sm.add_widget(Menu(name="menu"))
    sm.add_widget(MainWidget(name="main"))
    sm.add_widget(Progress(name="progress"))
    return sm

if __name__ == "__main__":
  CardsApp().run()