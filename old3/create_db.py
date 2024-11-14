import sqlite3



con = sqlite3.connect("base.db")
cur = con.cursor()
cur.execute(
  """CREATE TABLE IF NOT EXISTS cards(
    front CHAR,
    back CHAR,
    picture INT,
    status INT,
    prestatus INT,
    actiontime DATETIME,
    interval INT);
  """
  )
cur.execute(
  """CREATE TABLE IF NOT EXISTS users(
  name CHAR,
  round INT,
  step INT,
  time DATETIME);
  """
  )


con.commit()