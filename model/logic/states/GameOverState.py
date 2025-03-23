'''

@author Maurice Amon

@description Final state of the DFA, marks the end of the game, notify observers to display game over screen ..
'''
from model.GameHandler import GameHandler


class GameOverState:

    _game_handler = None
    def __init__(self):
        self._game_handler = GameHandler()


    def handle_action(self, object):
        pass