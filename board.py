import random
import logging
logger = logging.getLogger(__name__)


class Board:
    def __init__(self, max_row=1, max_column=1):
        assert max_row >= 1, f"Max row must be 1 or higher"
        self.max_row = max_row
        assert max_column >= 1, f"Max column must be 1 or higher"
        self.max_column = max_column
        self._board = [[False for c in range(self.max_column)] for r in range(self.max_row)]

    def get(self, row=0, column=0):
        return self._board[row % self.max_row][column % self.max_column]

    def set(self, row=0, column=0, state=True):
        self._board[row % self.max_row][column % self.max_column] = state

    def __str__(self):
        result = "-{:}-\n".format("-"*self.max_column)
        for r in range(self.max_row):
            result += "|"
            for c in range(self.max_column):
                result += "X" if self.get(r, c) else " "
            result += "|\n"
        result += "-{:}-".format("-"*self.max_column)
        return result

    def get_living_neighbours(self, row, column):
        # Nested for loops will also count cell(row, column), account for it
        living_neighbours = -1 if self.get(row, column) else 0
        for r in range(row-1, row+2):
            for c in range(column-1, column+2):
                if self.get(r, c):
                    living_neighbours += 1
        return living_neighbours


class BoardPair:
    def __init__(self, max_row=1, max_column=1):
        assert max_row >= 1, f"Max row must be 1 or higher"
        self.max_row = max_row
        assert max_column >= 1, f"Max column must be 1 or higher"
        self.max_column = max_column
        self._boards = (Board(max_row, max_column), Board(max_row, max_column))
        self._active_board = 0

    def get_active_board(self):
        return self._boards[self._active_board]

    def get_next_board(self):
        return self._boards[(self._active_board+1) % 2]

    def get(self, row=0, column=0):
        return self.get_active_board().get(row, column)

    def set(self, row=0, column=0, state=True):
        self.get_active_board().set(row, column, state)

    def __str__(self):
        result = 'Active\n'
        result += str(self.get_active_board())
        result += '\nNext\n'
        result += str(self.get_next_board())
        return result

    def flip(self):
        self._active_board = (self._active_board+1) % 2


def set_glider(row, column, board):
    board.set(row, column)
    board.set(row+1, column+1)
    board.set(row+1, column+2)
    board.set(row+2, column)
    board.set(row+2, column+1)


def set_random(board):
    for r in range(board.max_row):
        for c in range(board.max_column):
            if random.randint(0, 1):
                board.set(r, c)

