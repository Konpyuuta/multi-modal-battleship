'''

@author Maurice Amon
'''
from model.Player import Player


class Game:

    _player1 = None

    _player2 = None
    # 0: Start game; 1: Running game; 2: Game Over
    _game_state = 0

    _is_turn = None

    _winner = None

    def __init__(self, player1: Player, player2: Player):
        self._player1 = player1
        self._player2 = player2
        self._is_turn = player1

    def execute_move(self, col, row):
        battleship_matrix = None
        if self._is_turn == self._player1:
            battleship_matrix = self._player2.get_battleship_matrix()
        else:
            battleship_matrix = self._player1.get_battleship_matrix()


        battleship_matrix.set_bomb_in_matrix(col, row)
        if self._is_turn == self._player1:
            self._is_turn = self._player2
        else:
            self._is_turn = self._player1

    def check_is_game_over(self) -> bool:
        player1_battleship_matrix = self._player1.get_battleship_matrix().get_matrix()
        player2_battleship_matrix = self._player2.get_battleship_matrix().get_matrix()
        result1 = True
        result2 = True
        for x in range(10):
            for y in range(10):
                if player1_battleship_matrix[x][y] == 1:
                    result1 = False
                if player2_battleship_matrix[x][y] == 1:
                    result2 = False
        if result1 == True:
            self._winner = self._player1.get_name()
        elif result2 == True:
            self._winner = self._player2.get_name()

        if result1 or result2:
            self._game_state = 1

        return result1 or result2

    def get_player1(self):
        return self._player1

    def get_player2(self):
        return self._player2

    def get_player_by_ID(self, id):
        if self._player1.get_name() == id:
            return self._player1
        elif self._player2.get_name() == id:
            return self._player2


    def get_player1_battleship_matrix(self):
        return self._player1.get_battleship_matrix()

    def get_player2_battleship_matrix(self):
        return self._player2.get_battleship_matrix()

    def is_turn(self):
        return self._is_turn

    def get_game_state(self):
        return self._game_state

    def get_winner(self):
        return self._winner