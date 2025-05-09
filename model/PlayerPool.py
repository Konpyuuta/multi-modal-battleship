'''

@author Maurice Amon
@description The pool of players
'''
from abc import ABC


class PlayerPool(ABC):

    _player_pool = list()

    def add_player(self, player):
        self._player_pool.append(player)

    def remove_player(self, player):
        self._player_pool.remove(player)
