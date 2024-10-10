from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.properties import StringProperty, ColorProperty
from datetime import datetime, timedelta
import crud


class Menu(Screen):
  current_user = "default_user"
  def screens_order(self):
    user_result = crud.get_user(self.current_user)
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
  current_user = "default_user"
  user_db = crud.get_user(current_user)
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
    self.round = self.user_db[1]
    self.step = self.user_db[2]
    self.init_round_cards()
    self.front = self.round_cards[0][1]

  def init_users(self):
    if self.user_db == None:
      crud.create_user(self.current_user)
      self.user_db = crud.get_user(self.current_user)

  def init_cards(self):
    if self.cards_db == []:
      crud.create_default_cards()
      self.cards_db = crud.read_cards()

  def init_round_cards(self):
    self.round_cards = [
      i for i in self.cards_db[self.round * 11 + self.step : (self.round * 11 + self.step) + 11 - self.step]
    ]

    # self.round_cards = [
    #   i for i in self.cards_db[self.round * 11 + self.step : (self.round * 11 + self.step) + 11]
    # ]

    # self.round_cards = [
    #   i for i in self.cards_db[self.round * 11 + self.step : (self.round * 11 + self.step) + 11 - (self.round * 11 + self.step)]
    # ]
    # print(self.round * 11 + self.step, (self.round * 11 + self.step) + (11 - (self.round * 11 + self.step)))
    # print(self.round * 11 + self.step, (self.round * 11 + self.step) + 11)
    print(self.round * 11 + self.step, (self.round * 11 + self.step) + 11 - self.step)

    print(self.round_cards)



  # def init_repeat_cards(self):
  #   easy_cards = []
  #   good_cards = []
  #   again_cards = []
  #   hard_cards = []
  #   for i in self.cards_db[self.round * 11 + self.step : (self.round * 11 + self.step) + 11]:
  #     if i[4] == 1:
  #       easy_cards.append(i)
  #     elif i[4] == 2:
  #       good_cards.append(i)
  #     elif i[4] == 3:
  #       again_cards.append(i)
  #     else:
  #       hard_cards.append(i)


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
    if len(self.round_cards) > 0:
      self.front = self.round_cards[0][1]
    else:
      current_time = datetime.now()
      crud.update_round_time(
        self.current_user,
        current_time
      )
      self.manager.current = "progress"

  # def count_step(self):
  #   if self.step < 11:
  #     self.step += 1
  #   else:
  #     self.step = 1
  #     # self.step = 1
  #     self.round += 1

  def count_step(self):
    self.step += 1
    if self.step == 11:
      self.step = 0
      self.round += 1

  def rating(self, rating):
    self.count_step()
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
    crud.update_step(self.round, self.step, self.current_user)
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