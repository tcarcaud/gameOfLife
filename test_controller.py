import unittest
from unittest.mock import MagicMock, patch, call
from board import Board, BoardPair
import controller


class TestController(unittest.TestCase):
    def setUp(self):
        self.board = Board(4, 3)

    def test_empty_board(self):
        self.assertEqual(False, controller.next_state(0, 0, self.board))

    def test_next_state_come_alive(self):
        row = 1
        column = 1
        self.board.set(row-1, column-1)
        self.board.set(row-1, column)
        # Dead cell(row,column) has two living neighbours, it stays dead
        self.assertEqual(False, controller.next_state(row, column, self.board))
        self.board.set(row, column-1)
        # Dead cell(row,column) has three living neighbours, it comes alive
        self.assertEqual(True, controller.next_state(row, column, self.board))
        self.board.set(row+1, column-1)
        # Dead cell(row,column) has 4 living neighbours, it stays dead
        self.assertEqual(False, controller.next_state(row, column, self.board))

    def test_next_state_die(self):
        row = 1
        column = 1
        self.board.set(row, column)
        # Living cell(row,column) has no living neighbours, it dies
        self.assertEqual(False, controller.next_state(row, column, self.board))
        self.board.set(row-1, column-1)
        self.board.set(row-1, column)
        # Living cell(row,column) has two living neighbours, it stays alive
        self.assertEqual(True, controller.next_state(row, column, self.board))
        self.board.set(row, column-1)
        self.board.set(row+1, column-1)
        # Living cell(row,column) has four living neighbours, it dies
        self.assertEqual(False, controller.next_state(row, column, self.board))

    @patch('controller.next_state')
    def test_next_board_come_alive(self, next_state_mock):
        next_state_mock.return_value = True
        next_board = Board(4, 3)
        next_board.set = MagicMock()

        controller.next_board(self.board, next_board)
        # next_board loops over self.board and set next_state into next_board
        next_state_calls = [call(r, c, self.board) for r in range(self.board.max_row) for c in range(self.board.max_column)]
        next_state_mock.assert_has_calls(next_state_calls, any_order=True)
        set_calls = [call(r, c, True) for r in range(self.board.max_row) for c in range(self.board.max_column)]
        next_board.set.assert_has_calls(set_calls, any_order=True)


if __name__ == '__main__':
    unittest.main()
