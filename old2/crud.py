from create_db import cur, con
from datetime import datetime, timedelta


def read_cards():
  cur.execute("SELECT rowid, * FROM cards")
  return cur.fetchall()


def get_user(name):
  cur.execute(f"SELECT * FROM users WHERE name == '{name}'")
  return cur.fetchone()

def get_card(id):
  cur.execute((f"SELECT rowid, * FROM cards WHERE rowid == '{id}'"))
  return cur.fetchone()

def update_card_status(id, status):
  cur.execute(
    f"""UPDATE cards SET 
      status = '{status}' WHERE rowid == '{id}'""")
  con.commit()

def update_step(round, step, name):
  cur.execute(
    f"""UPDATE users SET 
      round = '{round}',
      step = '{step}' WHERE name == '{name}'""")
  con.commit()

def update_round_time(name, current_time):
  cur.execute(f"UPDATE users SET time = '{current_time}' WHERE name == '{name}'")
  con.commit()

def create_user(name):
  start_time = datetime.now() - timedelta(minutes=2)
  cur.execute(f"""INSERT INTO users VALUES('{name}', '0', '0', '{start_time}' )""")
  con.commit()


def create_default_cards():
  cards = [('АА', 'ананас', 1, 0), ('АБ', 'арбуз', 2, 0), ('АВ', 'аквариум', 3, 0), ('АГ', 'ангел', 4, 0), ('АД', 'андроид', 5, 0), ('АЕ','апельсин', 6, 0), ('АЖ','аджика', 7, 0), ('АЗ','абзац', 8, 0), ('АИ','адидас', 9, 0), ('АК','арка', 10, 0), ('АЛ','аллея', 11, 0), ('АМ','алмаз', 12, 0), ('АН','арнольд', 13, 0), ('АО','алоэ', 14, 0), ('АП','амплитуда', 15, 0), ('АР','абрикос', 16, 0), ('АС', 'аист', 17, 0), ('АТ', 'аптека', 18, 0), ('АУ', 'акула', 19, 0), ('АФ', 'алфавит', 20, 0), ('АХ', 'архыз', 21, 0), ('АЧ', 'анчоус', 22, 0), ('БА', 'биатлон', 23, 0), ('ББ', 'бабушка', 24, 0), ('БВ','бивень', 25, 0), ('БГ','бегемот', 26, 0), ('БД', 'бадминтон', 27, 0), ('БЕ', 'брелок', 28, 0), ('БЖ', 'бижутерия', 29, 0), ('БЗ', 'бизон', 30, 0), ('БИ', 'бритва', 31, 0), ('БК', 'букварь', 32, 0), ('БЛ', 'билет', 33, 0), ('БМ', 'бумеранг', 34, 0), ('БН', 'банан', 35, 0), ('БО', 'брови', 36, 0), ('БП', 'бип', 37, 0), ('БР', 'борода', 38, 0), ('БС', 'бассейн', 39, 0), ('БТ', 'батон', 40, 0), ('БУ', 'боулинг', 41, 0), ('БФ', 'бифштекс', 42, 0), ('БХ', 'бахилы', 43, 0), ('БЧ', 'бочка', 44, 0)]
  
  cur.executemany("INSERT INTO cards VALUES(?, ?, ?, ?)", cards)
  con.commit()
