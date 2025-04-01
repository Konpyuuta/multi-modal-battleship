'''

@author Maurice Amon

@description Final state of the DFA, marks the end of the game, notify observers to display game over screen ..
'''


class GameOverState:

    _game_handler = None

    def __init__(self, game_handler):
        self._game_handler = game_handler


    def handle_action(self, object):
        pass