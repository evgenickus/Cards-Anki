from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.properties import StringProperty, ColorProperty
from datetime import datetime, timedelta
import crud

count_one = 0
count_two = 0
count_tree = 0

def update_count():
  cards_db = crud.read_cards()
  return cards_db

class Menu(Screen):
  current_user = "default_user"
  def screens_order(self):
    user_result = crud.get_user(self.current_user)
    last_action = user_result[3]
    action_time = datetime.fromisoformat(last_action)
    next_time = action_time + timedelta(minutes=15)
    can_next_round = datetime.now() > next_time
    if can_next_round:
      self.manager.current = "main"
    else:
      self.manager.current = "progress"

class Progress(Screen):
  global update_count
  cards = update_count()
  print(cards)
  card = StringProperty('cards[1][1]')

class MainWidget(Screen):
  current_user = "default_user"
  user_db = crud.get_user(current_user)
  cards_db = crud.read_cards()
  step = 0
  round = 0
  NEW_CARDS_NUMBER = 11


  current_card = list()
  new_cards = list()
  inround_cards = list()
  studied_cards = list()
  LEARNING_STEP1 = 1
  LEARNING_STEP2 = 10
  HARD_INL = int(LEARNING_STEP2 / LEARNING_STEP1)
  GRADUATING_INL = 1440
  EASY_INL = 5760
  EASY = 2.5



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
    self.init_other_cards()
    self.init_new_cards()
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

  def init_count_labels(self):
    self.new = str(len(self.new_cards))
    self.inround = str(len(self.inround_cards))
    self.studied = str(len(self.studied_cards))

  def init_underline(self):
    if int(self.new) > 0:
      self.ids.new.underline = True
      self.ids.inround.underline = False
      self.ids.studied.underline = False
    elif int(self.new) == 0 and int(self.inround) > 0:
      self.ids.new.underline = False
      self.ids.inround.underline = True
      self.ids.studied.underline = False
    elif (int(self.new) == 0 and int(self.inround) == 0) and int(self.studied) > 0:
      self.ids.new.underline = False
      self.ids.inround.underline = False
      self.ids.studied.underline = True

  
  def init_new_cards(self):
    if self.user_db[4] == 1:
      self.new_cards = [
        i for i in self.cards_db[
          self.round * self.NEW_CARDS_NUMBER + self.step : (self.round * self.NEW_CARDS_NUMBER + self.step) + self.NEW_CARDS_NUMBER - self.step
        ] if i[4] == 0
      ]
    else:
      self.new_cards = list()

  def init_other_cards(self):
    round_cards = crud.read_round_cards()
    print(round_cards)
    for i in round_cards:
      if i[4] in [1, 5]:
        self.studied_cards.append(i)
      elif i[4] in [2, 3, 4]:
        self.inround_cards.append(i)
  

  def init_current_card(self):
    if len(self.new_cards) > 0:
      self.current_card = self.new_cards[0]
      self.front = self.current_card[1]
    elif len(self.new_cards) == 0 and len(self.inround_cards) > 0:
      self.current_card = self.inround_cards[0]
      self.front = self.current_card[1]
    elif len(self.new_cards) == 0 and len(self.inround_cards) == 0 and len(self.studied_cards) > 0:
      self.current_card = self.studied_cards[0]
      self.front = self.current_card[1]


  def get_next_card(self):
    if len(self.new_cards) > 0:
      if len(self.new_cards) != 0:
        self.current_card = self.new_cards[0]
        self.front = self.current_card[1]
      elif len(self.new_cards) == 0 and len(self.inround_cards) > 0:
        self.current_card = self.inround_cards[0]
        self.front = self.current_card[1]
      elif len(self.new_cards) == 0 and len(self.inround_cards) == 0 and len(self.studied_cards) > 0:
        crud.update_start_new_cards(self.current_user, 0)
        self.current_card = self.studied_cards[0]
        self.front = self.current_card[1]
      else:
        self.stop_round()
    elif len(self.new_cards) == 0 and len(self.inround_cards) > 0:
      if len(self.inround_cards) != 0:
        self.current_card = self.inround_cards[0]
        self.front = self.current_card[1]
      elif len(self.new_cards) == 0 and len(self.inround_cards) == 0 and len(self.studied_cards) > 0:
        crud.update_start_new_cards(self.current_user, 0)
        self.current_card = self.studied_cards[0]
        self.front = self.current_card[1]
      else:
        self.stop_round()
    elif len(self.new_cards) == 0 and len(self.inround_cards) == 0 and len(self.studied_cards) > 0:
      crud.update_start_new_cards(self.current_user, 0)
      if len(self.studied_cards) != 0:
        self.current_card = self.studied_cards[0]
        self.front = self.current_card[1]
      else:
        self.stop_round()
    else:
      self.stop_round()

  def stop_round(self):
    current_time = datetime.now()
    crud.update_round_time(self.current_user, current_time, 1)
    self.manager.current = "progress"
    self.init_new_cards()
    self.init_current_card()

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
    if self.step == self.NEW_CARDS_NUMBER:
      self.step = 0
      self.round += 1

  def easy_action(self):
    status = 1
    card_db = crud.get_card(self.current_card[0])
    prestatus = card_db[4]
    if prestatus == 0:
      self.new_cards.remove(self.current_card)
      self.count_step()
    elif prestatus in [1, 5]:
      self.studied_cards.remove(self.current_card)
    else:
      self.inround_cards.remove(self.current_card)
      if card_db[5] == 0:
        self.count_step()
    actiontime = datetime.now()
    interval = actiontime + timedelta(minutes=60)
    crud.update_card_status(self.current_card[0], status, 1, actiontime, interval)

  def hard_action(self):
    card_db = crud.get_card(self.current_card[0])
    prestatus = card_db[4]
    actiontime = datetime.now()
    interval = actiontime
    if prestatus == 0:
      status = 3
      self.new_cards.remove(self.current_card)
      self.inround_cards.append(self.current_card)
      crud.update_card_status(self.current_card[0], status, card_db[5], actiontime, interval)
    elif prestatus in [1, 5]:
      status = 4
      self.studied_cards.remove(self.current_card)
      self.inround_cards.append(self.current_card)
      crud.update_card_status(self.current_card[0], status, card_db[5], actiontime, interval)
    elif prestatus == 3:
      status = 3
      self.inround_cards.remove(self.current_card)
      self.inround_cards.append(self.current_card)
      crud.update_card_status(self.current_card[0], status, card_db[5], actiontime, interval)


  def again_action(self):
    card_db = crud.get_card(self.current_card[0])
    prestatus = card_db[4]
    actiontime = datetime.now()
    status = 3
    interval = actiontime
    if prestatus == 0:
      self.new_cards.remove(self.current_card)
      self.inround_cards.append(self.current_card)
    elif prestatus in [1, 5]:
      self.studied_cards.remove(self.current_card)
      self.inround_cards.append(self.current_card)
    else:
      self.inround_cards.remove(self.current_card)
      self.inround_cards.append(self.current_card)
    crud.update_card_status(self.current_card[0], status, card_db[5], actiontime, interval)

  def good_action(self):
    card_db = crud.get_card(self.current_card[0])
    prestatus = card_db[4]
    actiontime = datetime.now()
    if prestatus == 0:
      status = 2
      self.new_cards.remove(self.current_card)
      self.inround_cards.append(self.current_card)
      interval = actiontime
      crud.update_card_status(self.current_card[0], status, card_db[5], actiontime, interval)
    elif prestatus == 1:
      status = 2
      self.studied_cards.remove(self.current_card)
      self.inround_cards.append(self.current_card)
      interval = actiontime
      crud.update_card_status(self.current_card[0], status, card_db[5], actiontime, interval)    
    elif prestatus in [2, 4]:
      status = 5
      interval = actiontime + timedelta(minutes=15)
      self.inround_cards.remove(self.current_card)
      if card_db[5] == 0:
        self.count_step()
      crud.update_card_status(self.current_card[0], status, 1, actiontime, interval)
    elif prestatus == 3:
      status = 2
      self.inround_cards.remove(self.current_card)
      self.inround_cards.append(self.current_card)
      interval = actiontime
      crud.update_card_status(self.current_card[0], status, card_db[5], actiontime, interval)
    elif prestatus == 5:
      status = 5
      interval = actiontime + timedelta(minutes=15)
      crud.update_card_status(self.current_card[0], status, card_db[5], actiontime, interval)
      self.studied_cards.remove(self.current_card)





  def rating(self, rating):
    self.picture_link = ""
    self.back = ""
    self.change_widget_rating()

    if rating == "easy":
      self.easy_action()
    elif rating == "good":
      self.good_action()
    elif rating == "again":
      self.again_action()
    elif rating == "hard":
      self.hard_action()

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