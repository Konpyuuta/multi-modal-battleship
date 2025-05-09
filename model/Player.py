'''

@author Maurice Amon

Represents a player
'''
from model.board.BattleshipMatrix import BattleshipMatrix


class Player:

    _ip = None

    _port = None

    _name = None

    _is_turn = None

    _battleships = None

    _battleship_matrix = None

    _opponent_battleship_matrix = None

    _heart_rate = 0.0

    def __init__(self, ip, port, name, is_turn, battleships: BattleshipMatrix):
        self._ip = ip
        self._port = port
        self._name = name
        self._is_turn = is_turn
        self._battleships = battleships

    def set_name(self, name):
        self._name = name

    def set_is_turn(self, is_turn):
        self._is_turn = is_turn

    def set_battleships(self, battleships):
        self._battleships = battleships


    def set_battleship_matrix(self, battleship_matrix):
        self._battleship_matrix = battleship_matrix

    def set_opponent_battleship_matrix(self, opponent_battleship_matrix):
        self._opponent_battleship_matrix = opponent_battleship_matrix


    def set_heart_rate(self, heart_rate):
        self._heart_rate = heart_rate

    def get_name(self):
        return self._name

    def get_is_turn(self):
        return self._is_turn

    def get_battleship_matrix(self):
        return self._battleship_matrix

    def get_opponent_battleship_matrix(self):
        return self._opponent_battleship_matrix


    def get_heart_rate(self):
        return self._heart_rate