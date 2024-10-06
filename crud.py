from create_db import cur, con
from datetime import datetime, timedelta

def get_words():
  cur.execute("SELECT front FROM cards")
  return cur.fetchall()

def get_user(name):
  cur.execute(f"SELECT * FROM users WHERE name == '{name}'")
  return cur.fetchone()

def create_default_user(name):
  start_time = datetime.now() - timedelta(minutes=2)
  cur.execute(f"""INSERT INTO users VALUES('{name}', '0', '0', '', '', '', '{start_time}' )""")
  con.commit()


def create_default_cards():
  cards = [('АА', 'ананас', 1), ('АБ', 'арбуз', 2), ('АВ', 'аквариум', 3), ('АГ', 'ангел', 4), ('АД', 'андроид', 5), ('АЕ','апельсин', 6), ('АЖ','аджика', 7), ('АЗ','абзац', 8), ('АИ','адидас', 9), ('АК','арка', 10), ('АЛ','аллея', 11), ('АМ','алмаз', 12), ('АН','арнольд', 13), ('АО','алоэ', 14), ('АП','амплитуда', 15), ('АР','абрикос', 16), ('АС', 'аист', 17), ('АТ', 'аптека', 18), ('АУ', 'акула', 19), ('АФ', 'алфавит', 20), ('АХ', 'архыз', 21), ('АЧ', 'анчоус', 22), ('БА', 'биатлон', 23), ('ББ', 'бабушка', 24), ('БВ','бивень', 25), ('БГ','бегемот', 26), ('БД', 'бадминтон', 27), ('БЕ', 'брелок', 28), ('БЖ', 'бижутерия', 29), ('БЗ', 'бизон', 30), ('БИ', 'бритва', 31), ('БК', 'букварь', 32), ('БЛ', 'билет', 33), ('БМ', 'бумеранг', 34), ('БН', 'банан', 35), ('БО', 'брови', 36), ('БП', 'бип', 37), ('БР', 'борода', 38), ('БС', 'бассейн', 39), ('БТ', 'батон', 40), ('БУ', 'боулинг', 41), ('БФ', 'бифштекс', 42), ('БХ', 'бахилы', 43), ('БЧ', 'бочка', 44)]
  
  cur.executemany("INSERT INTO cards VALUES(?, ?, ?)", cards)
  con.commit()

def find_word(letters):
  cur.execute(f"SELECT back, picture FROM cards WHERE front == '{letters}'")
  return cur.fetchone()

def upgrade_rating(name, round, step, day_cards, repeat_cards, inround_cards):
  cur.execute(
    f"""UPDATE users SET 
      round = '{round}',
      step = '{step}',
      day_cards = '{day_cards}',
      inround_cards = '{inround_cards}',
      repeat_cards = '{repeat_cards}' WHERE name == '{name}'""")
  con.commit()

def stop_round(name, round, step, day_cards, repeat_cards, inround_cards, current_time):
  cur.execute(
    f"""UPDATE users SET 
      round = '{round}',
      step = '{step}',
      day_cards = '{day_cards}',
      inround_cards = '{inround_cards}',
      repeat_cards = '{repeat_cards}',
      time = '{current_time}' WHERE name == '{name}'""")
  con.commit()