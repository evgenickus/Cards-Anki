import crud
new_cards = list()
inround_cards = list()
studied_cards = list()
cards_db = crud.read_cards()
current_user = "default_user"
user_db = crud.get_user(current_user)
round = user_db[1]
step = user_db[2]
current_card = list()

def init_cards_rating():
  global new_cards, inround_cards, studied_cards, round, step
  new_cards = [i for i in cards_db[round * 11 + step : (round * 11 + step) + 11 - step]]
  inround_cards = [i for i in cards_db if i[4] in [3, 4]]
  studied_cards = [i for i in cards_db if i[4] in [1, 2]]


def get_current_cards():
  global current_card
  if len(inround_cards) == 0 and len(new_cards) > 0:
    current_card = new_cards[0]
    new_cards.remove(new_cards[0])
  elif len(new_cards) == 0 and len(inround_cards) > 0:
    current_card = inround_cards[0]
    inround_cards.remove(inround_cards[0])
  

init_cards_rating()
get_current_cards()
print(current_card)




