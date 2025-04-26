'''

@author Maurice Amon
'''
from model.states.State import State


class GameOverState(State):

    def __init__(self, game_handler):
        self._game_handler = game_handler


    def handle_action(self, object):
        game = self._game_handler.get_game()
