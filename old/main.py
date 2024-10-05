from kivy.config import Config
# Config.set('graphics', 'width', 450)
# Config.set('graphics', 'height', 750)

from kivy.app import App
from kivy.properties import ColorProperty, StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from datetime import datetime, timedelta
import crud



class Menu(Screen):

  def screens_order(self):
    user_result = crud.find_user("default_user")
    last_action = user_result[0][3]
    action_time = datetime.fromisoformat(last_action)
    next_time = action_time + timedelta(minutes=2)
    can_next_step = datetime.now() > next_time
    print(can_next_step)
    if can_next_step:
      self.manager.current = "main"
    else:
      self.manager.current = "new"

class New(Screen):
  pass
  # cards_counter = StringProperty("10")
  # new_cards_counter = StringProperty("0")
  # repeat_cards_counter = StringProperty("0")

  # def __init__(self, **kw):
  #   super(New, self).__init__(**kw)
  #   self


class MainWidget(Screen):
  card_letter_list = ['Ч', 'Х', 'Ф', 'У', 'Т', 'С', 'Р', 'П', 'О', 'Н', 'М', 'Л', 'К', 'И', 'З', 'Ж', 'Е', 'Д', 'Г', 'В', 'Б', 'А']
  words_list = ['АНАНАС', 'АРБУЗ', 'АКВАРИУМ', 'АНГЕЛ', 'АНДРОИД', 'АПЕЛЬСИН', 'АДЖИКА', 'АБЗАЦ', 'АДИДАС', 'АРКА', 'АЛЛЕЯ', 'АЛМАЗ', 'АРНОЛЬД', 'АЛОЭ', 'АМПЛИТУДА', 'АБРИКОС', 'АИСТ', 'АПТЕКА', 'АКУЛА', 'АЛФАВИТ', 'АРХЫЗ', 'АНЧОУС', 'БИАТЛОН', 'БАБУШКА', 'БИВЕНЬ', 'БЕГЕМОТ', 'БАДМИНТОН', 'БРЕЛОК', 'БИЖУТЕРИЯ', 'БИЗОН', 'БРИТВА', 'БУКВАРЬ', 'БИЛЕТ', 'БУМЕРАНГ', 'БАНАН', 'БРОВИ', 'БИП', 'БОРОДА', 'БАССЕЙН', 'БАТОН', 'БОУЛИНГ', 'БИФШТЕКС', 'БАХИЛЫ', 'БОЧКА']
  letter_num_a = 21
  letter_num_b = 21
  letter_a = StringProperty(card_letter_list[letter_num_a])
  letter_b = StringProperty(card_letter_list[letter_num_b])
  underline_cards_counter = ObjectProperty(True)
  underline_new_cards_counter = ObjectProperty(False)
  underline_repeat_cards_counter = ObjectProperty(False)
  word = StringProperty("")
  word_db = str()
  cards_counter = StringProperty("10")
  new_cards_counter = StringProperty("0")
  repeat_cards_counter = StringProperty("0")
  picture_link = StringProperty("")
  active_user = "default_user"
  can_next_step = True
  rounds = int()
  step = int(1)


  def __init__(self, **kwargs):
    super(MainWidget, self).__init__(**kwargs)
    self.read_player_results()
    self.ids.main_widget.remove_widget(self.ids.box_level)
    self.ids.box_letter.remove_widget(self.ids.lab3)
    self.ids.box_letter.remove_widget(self.ids.picture)
    self.ids.main_widget.remove_widget(self.ids.message_box)


  def read_player_results(self):
    user_result = crud.find_user("default_user")
    self.rounds, self.step = user_result[0][1], user_result[0][2]
    last_action = datetime.fromisoformat(user_result[0][3])
    next_time = last_action + timedelta(minutes=2)
    self.can_next_step = datetime.now() > next_time

  def rating_word(self, rating):
    crud.add_task(self.word_db, rating)
    self.reset()
    self.count_round()
    self.count_cards_counter()

  def end_of_round(self):
    self.manager.current = "new"


  def find_word(self):
    tempory_word_list = []
    for word in self.words_list:
      if self.letter_a == word[0]:
        tempory_word_list.append(word)
    for word in tempory_word_list:
      if self.letter_b == word[2]:
        self.ids.lab3.font_size = int(150 - len(word) * 2)
        self.word_db = word
        self.word = f"[color=008eff][u]{word[0]}[/u][/color]{word[1].lower()}[color=008eff][u]{word[2]}[/u][/color]{word[3:].lower()}"
        self.picture_link = f"images/{str(self.words_list.index(word)+1)}.jpg"


  def reset(self):
    self.ids.box_letter.orientation = "horizontal"
    self.ids.box_letter.add_widget(self.ids.lab1)
    self.ids.box_letter.add_widget(self.ids.lab2)
    self.ids.box_letter.remove_widget(self.ids.lab3)
    self.ids.box_letter.remove_widget(self.ids.picture)
    self.ids.main_widget.add_widget(self.ids.but_open)
    self.ids.main_widget.remove_widget(self.ids.box_level)
    self.word = ""
    self.picture_link = ""

  def count_cards_counter(self):
    if int(self.cards_counter) > 0:
      count = int(self.cards_counter) - 1
    else:
      count = '10'
    self.cards_counter = str(count)
    

  def count_index_a_b(self):
    if self.letter_num_b > 0:
      self.letter_num_b -= 1
    else:
      self.letter_num_b = 21
      self.letter_num_a -= 1
    if self.letter_a == 0:
      self.letter_a = 21

  def count_round(self):
    if self.step == 10:
      self.step = 0
      self.rounds += 1
      crud.save_progress(self.active_user, self.rounds, self.step, self.cards_counter, self.new_cards_counter, self.repeat_cards_counter)
      self.end_of_round()
    else:
      self.step += 1

  def open_card(self):
    self.ids.box_letter.orientation = "vertical"
    self.ids.box_letter.remove_widget(self.ids.lab1)
    self.ids.box_letter.remove_widget(self.ids.lab2)
    self.ids.box_letter.add_widget(self.ids.lab3)
    self.ids.box_letter.add_widget(self.ids.picture)
    self.ids.main_widget.remove_widget(self.ids.but_open)
    self.ids.main_widget.add_widget(self.ids.box_level)
    self.find_word()
    self.count_index_a_b()
    self.letter_a = self.card_letter_list[self.letter_num_a]
    self.letter_b = self.card_letter_list[self.letter_num_b]

class Cards(App):
  main_color = ColorProperty([255/255, 122/255, 0, 1])
  
  def build(self):
    sm = ScreenManager(transition=FadeTransition())
    sm.add_widget(Menu(name="menu"))
    sm.add_widget(MainWidget(name="main"))
    sm.add_widget(New(name="new"))

    return sm

Cards().run()