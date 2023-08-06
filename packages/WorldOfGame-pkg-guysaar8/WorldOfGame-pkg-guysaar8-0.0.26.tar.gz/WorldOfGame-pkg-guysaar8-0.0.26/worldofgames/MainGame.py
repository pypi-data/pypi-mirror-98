#####################
# Import modules
#####################
from worldofgames.UserAccount import loging, welcome
from worldofgames.Live import load_game
from worldofgames.ManegeGame import GameManager


#####################
# Define Functions
#####################

def log():
    # initiate login
    user = loging()
    welcome(user)
    return user


def start():
    # pick a game
    load_game_list = load_game()
    game_id = load_game_list[0]
    difficulty = load_game_list[1]

    print("You will Play = ", game_id, "Difficulty = ", difficulty)

    # load the chosen game

    game_to_play = GameManager(game_id, difficulty)
    game_to_play.run(game_id, difficulty)


#####################
# START
#####################

log()

start()
