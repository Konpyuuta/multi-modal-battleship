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

    def __init__(self, player1: Player, player2: Player):
        self._player1 = player1
        self._player2 = player2

    def execute_move(self, col, row):
        battleship_matrix = None
        if self._is_turn:
            battleship_matrix = self._player2.get_battleship_matrix()
        else:
            battleship_matrix = self._player1.get_battleship_matrix()

        battleship_matrix.set_bomb_in_matrix(col, row)
        self._is_turn = not self._is_turn


    def check_is_game_over(self) -> bool:
        player1_battleship_matrix = self._player1.get_battleship_matrix()
        player2_battleship_matrix = self._player2.get_battleship_matrix()
        for x in range(10):
            for y in range(10):
                if player1_battleship_matrix[x][y] == 1 or player2_battleship_matrix[x][y] == 1:
                    return False

        return True


