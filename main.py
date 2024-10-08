from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.properties import StringProperty, ColorProperty
from datetime import datetime, timedelta
import crud

class Menu(Screen):
  def screens_order(self):
    user_result = crud.get_user("default_user")
    last_action = user_result[6]
    action_time = datetime.fromisoformat(last_action)
    next_time = action_time + timedelta(minutes=2)
    can_next_round = datetime.now() > next_time
    if can_next_round:
      self.manager.current = "main"
    else:
      self.manager.current = "progress"

class Progress(Screen):
  studied = StringProperty("")
  def __init__(self, **kw):
    super(Progress, self).__init__(**kw)
    user = crud.get_user("default_user")
    user_result = len([i for i in user[5].split(",") if i != ""])
    self.studied = f"Изучено карточек: {user_result}"

  # if self.studied is not None:
  # else:
  #   user = crud.get_user("default_user")
  #   self.studied = ""

class MainWidget(Screen):
  step = 0
  round = 0
  cards_db = crud.read_cards()
  cards = [i[1] for i in cards_db]
  user = crud.get_user("default_user")

  if user is not None:
    day_cards_list = user[3].split(",")
  else:
    day_cards_list = list()

  repeat_cards = str()
  inround_cards = str()
  all_day_cards = list()

  front = StringProperty("")
  back = StringProperty("")
  new = StringProperty("")
  inround = StringProperty("")
  studied = StringProperty(repeat_cards)

  picture_link = StringProperty("")


  def __init__(self, **kw):
    super(MainWidget, self).__init__(**kw)
    self.ids.main_box.remove_widget(self.ids.rating_box)
    if self.user == None:
      crud.create_default_user("default_user")
      self.user = crud.get_user("default_user")
    if self.cards == []:
      crud.create_default_cards()
      self.cards_db = crud.read_cards()
      self.cards = [i[1] for i in self.cards_db]
    self.inround_cards = self.user[4]
    self.repeat_cards = self.user[5]
    self.round = self.user[1]
    self.step = self.user[2]
    if self.day_cards_list == [''] or self.day_cards_list == []:
      self.day_cards_list = [i for i in self.cards[self.round * 11 + self.step : (self.round * 11 + self.step) + 11]]
    else:
      self.day_cards_list = self.user[3].split(",")
    self.new = str(len(self.day_cards_list))
    self.inround = str(len([i for i in self.inround_cards.split(",") if i != ""]))
    self.studied = str(len([i for i in self.repeat_cards.split(",") if i != ""]))
    self.all_day_cards = [i for i in self.day_cards_list + self.inround_cards.split(",") if i != ""]
    self.front = self.all_day_cards[0]
    self.init_underline()

    self.init_cards_progress()


  def init_cards_progress(self):
    cards = crud.read_cards()
    cards_id = [i[0] for i in cards]
    print(cards_id)
  
  def init_underline(self):
    if int(self.new) > 0:
      self.ids.new.underline = True
      self.ids.inround.underline = False
    elif int(self.new) == 0:
      self.ids.new.underline = False
      self.ids.inround.underline = True
    

  def count_step(self):
    if self.step < 11:
      self.step += 1
    else:
      self.step = 1
      self.round += 1

  def remove_cards(self, card, address):
    if address == 1:
      cards_dict = self.inround_cards.split(",")
      if card in cards_dict:
          cards_dict.remove(card)
      self.inround_cards = ",".join(cards_dict)
    elif address == 2:
      cards_dict = self.repeat_cards.split(",")
      if card in cards_dict:
          cards_dict.remove(card)
      self.repeat_cards = ",".join(cards_dict)
    elif address == 3:
      cards_dict = self.day_cards_list
      if card in cards_dict:
        cards_dict.remove(card)
        self.day_cards_list = cards_dict

  def style_back(self, back):
    return f"[color=008eff][u]{back[0]}[/u][/color]{back[1].lower()}[color=008eff][u]{back[2]}[/u][/color]{back[3:].lower()}"

  def add_cards(self, card, address):
    if address == 1:
      cards_dict = self.inround_cards.split(",")
      if card not in cards_dict:
        cards_dict.append(card)
      self.inround_cards = ",".join(cards_dict)
    elif address == 2:
      cards_dict = self.repeat_cards.split(",")
      if card not in cards_dict:
        cards_dict.append(card)
      self.repeat_cards = ",".join(cards_dict)
    
  def rating(self, id):
    self.picture_link = ""
    self.ids.main_box.remove_widget(self.ids.rating_box)
    self.ids.main_box.add_widget(self.ids.open_button)
    if id == "again" or id == "hard":
      self.add_cards(self.front, 1)
      self.remove_cards(self.front, 2)
      self.remove_cards(self.front, 3)
    else:
      self.add_cards(self.front, 2)
      self.remove_cards(self.front, 1)
      self.remove_cards(self.front, 3)
      self.count_step()
    crud.upgrade_rating(self.user[0], self.round, self.step, ",".join(self.day_cards_list), self.repeat_cards, self.inround_cards)
    self.update_card_data()
    self.update_card_count()
    self.all_day_cards = [i for i in self.day_cards_list + self.inround_cards.split(",") if i != ""]
    if len(self.all_day_cards) > 0:
      self.front = self.all_day_cards[0]
    else:
      current_time = datetime.now()
      crud.stop_round(
        self.user[0],
        self.round,
        self.step,
        ",".join(self.day_cards_list),
        self.repeat_cards,
        self.inround_cards,
        current_time
      )
      self.manager.current = "progress"
      

  def update_card_count(self):
    self.new = str(len(self.day_cards_list))
    self.init_underline()
    self.inround = str(len([i for i in self.inround_cards.split(",") if i != ""]))
    self.studied = str(len([i for i in self.repeat_cards.split(",") if i != ""]))

  def update_card_data(self):
    self.user = crud.get_user("default_user")
    self.round = self.user[1]
    self.step = self.user[2]
    self.cards = crud.get_words()
    self.back = ""

  def change_widget(self):
    self.ids.main_box.remove_widget(self.ids.open_button)
    self.ids.main_box.add_widget(self.ids.rating_box)

  def style_back(self, back):
    return f"[color=008eff][u]{back[0].upper()}[/u][/color]{back[1]}[color=008eff][u]{back[2].upper()}[/u][/color]{back[3:]}"  

  def find_word(self, letters):
    res = crud.find_word(letters)
    print(self.all_day_cards)
    print(res)
    self.back = self.style_back(str(res[0]))
    self.picture_link = f"images/{res[1]}.jpg"

  def open_card(self):
    self.find_word(self.front)
    self.change_widget()


class AnkiApp(App):
  main_color = ColorProperty([255/255, 122/255, 0, 1])

  def build(self):
    sm = ScreenManager(transition=FadeTransition())
    sm.add_widget(Menu(name="menu"))
    sm.add_widget(MainWidget(name="main"))
    sm.add_widget(Progress(name="progress"))
    return sm

if __name__ == "__main__":
  AnkiApp().run()