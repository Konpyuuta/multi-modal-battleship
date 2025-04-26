'''

@author Maurice Amon
'''
import os
import random
from random import randrange


class BattleshipMatrix():

    # The values of the matrix can be 3 different values ..
    # 0: No ship, no bomb landed.
    # -1: No ship, a bomb landed. 1: A ship is there. 2: A ship is there and a bomb landed on it.
    _matrix = None
    # All different sizes of battleships ..
    _battleship_sizes = [2, 2]

    def __init__(self):
        rows, columns = (10, 10)
        self._matrix = [[0 for i in range(columns)] for j in range(rows)]


    def get_matrix(self):
        return self._matrix

    def set_matrix(self, matrix):
        self._matrix = matrix


    def has_bomb_been_placed(self, column, row):
        if self._matrix[column][row] == -1 or self._matrix[column][row] == 2:
            return True
        return False

    def set_bomb_in_matrix(self, column, row):
        if self._matrix[column][row] == 0:
            self._matrix[column][row] = -1
            return False
        elif self._matrix[column][row] == 1:
            self._matrix[column][row] = 2
            return True


    def create_battleships(self):
        for i in self._battleship_sizes:
            coords = self.place_battleships(9, 9, i)
            self.insert_battleships(coords)


    def place_battleships(self, column, row, size):
        coordinates = []
        is_valid = False
        while not is_valid:
            direction = random.choice(["horizontal", "vertical"])
            if direction == "horizontal":
                col = random.randint(0, column - size)
                r = random.randint(0, row)
                if all(self._matrix[r][col + i] == 0 for i in range(size)):
                    is_valid = True
                    for i in range(size):
                        coordinates.append((r, col + i))
                    break

            else:
                r = random.randint(0, row - size)
                col = random.randint(0, column)
                if all(self._matrix[r + i][col] == 0 for i in range(size)):
                    is_valid = True
                    for i in range(size):
                        coordinates.append((r + i, col))
                    break

        return coordinates

    def insert_battleships(self, coords):
        for i, j in coords:
            self._matrix[i][j] = 1
        self.print_matrix()

    def print_matrix(self):
        st = ""
        for i in range(10):
            s = ""
            for j in range(10):
                s += f'''| {self._matrix[i][j]} '''

            st += f'''{s}{os.linesep}'''

        print(st, sep=f'''{os.linesep}''')
