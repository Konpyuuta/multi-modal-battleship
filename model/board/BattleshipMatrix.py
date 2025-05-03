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
    # All different sizes of battleships
    _battleship_sizes = [2, 2, 4, 5, 5, 4]
    # Store the coordinates of all ships
    _ships = []

    def __init__(self):
        rows, columns = (10, 10)
        self._matrix = [[0 for i in range(columns)] for j in range(rows)]
        self._ships = []

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
            # find which ship this cell belongs to
            ship_coords = self.find_ship_by_coord(column, row)
            if ship_coords:
                # sink the entire ship
                for ship_row, ship_col in ship_coords:
                    self._matrix[ship_row][ship_col] = 2
            #     self._ships.remove(ship_coords)
            # self._matrix[column][row] = 2
            return True

    def find_ship_by_coord(self, column, row):
        """Find the ship coordinates by the given cell coordinates"""
        for ship in self._ships:
            if (column, row) in ship:
                return ship
        return None

    def create_battleships(self):
        for i in self._battleship_sizes:
            coords = self.place_battleships(9, 9, i)
            self.insert_battleships(coords)

    def is_valid_placement(self, row, col, size, direction):
        """Check if a ship can be placed at the given position with proper spacing"""
        if direction == "horizontal":
            # Check if ship fits in bounds
            if col + size > 10:
                return False

            # Check the ship position and surrounding area (excluding diagonal)
            for i in range(size):
                # Check the ship cell itself
                if self._matrix[row][col + i] != 0:
                    return False

                # Check surrounding cells (up, down, left, right)
                # Up
                if row > 0 and self._matrix[row - 1][col + i] != 0:
                    return False
                # Down
                if row < 9 and self._matrix[row + 1][col + i] != 0:
                    return False
                # Left
                if i == 0 and col > 0 and self._matrix[row][col - 1] != 0:
                    return False
                # Right
                if i == size - 1 and col + size < 10 and self._matrix[row][col + size] != 0:
                    return False

        else:  # vertical
            # Check if ship fits in bounds
            if row + size > 10:
                return False

            # Check the ship position and surrounding area (excluding diagonal)
            for i in range(size):
                # Check the ship cell itself
                if self._matrix[row + i][col] != 0:
                    return False

                # Check surrounding cells (up, down, left, right)
                # Left
                if col > 0 and self._matrix[row + i][col - 1] != 0:
                    return False
                # Right
                if col < 9 and self._matrix[row + i][col + 1] != 0:
                    return False
                # Up
                if i == 0 and row > 0 and self._matrix[row - 1][col] != 0:
                    return False
                # Down
                if i == size - 1 and row + size < 10 and self._matrix[row + size][col] != 0:
                    return False

        return True

    def place_battleships(self, column, row, size):
        coordinates = []
        is_valid = False
        attempts = 0
        max_attempts = 1000  # Limit attempts to avoid infinite loop

        while not is_valid and attempts < max_attempts:
            direction = random.choice(["horizontal", "vertical"])

            if direction == "horizontal":
                col = random.randint(0, column - size)
                r = random.randint(0, row)

                if self.is_valid_placement(r, col, size, "horizontal"):
                    is_valid = True
                    for i in range(size):
                        coordinates.append((r, col + i))

            else: # vertical
                r = random.randint(0, row - size)
                col = random.randint(0, column)

                if self.is_valid_placement(r, col, size, "vertical"):
                    is_valid = True
                    for i in range(size):
                        coordinates.append((r + i, col))

            attempts += 1

        if not is_valid:
            print(f"Could not place battleship of size {size} after {max_attempts} attempts.")

        return coordinates

    def insert_battleships(self, coords):
        # Store the coordinates of the ship
        if coords:
            self._ships.append(coords)

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
