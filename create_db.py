import sqlite3



con = sqlite3.connect("base.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS cards(front CHAR, back CHAR, picture INT)")
cur.execute(
  """CREATE TABLE IF NOT EXISTS users(
  name CHAR,
  round INT,
  step INT,
  day_cards TEXT,
  inround_cards TEXT,
  repeat_cards TEXT,
  time DATETIME);
  """
  )


con.commit()