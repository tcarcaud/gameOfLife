from unittest import TestCase
from board import Board, BoardPair, set_glider


class TestBoard(TestCase):

    def setUp(self):
        self.board = Board(3, 4)

    def test_construction_invalid_max_row(self):
        with self.assertRaisesRegex(AssertionError, "Max row must be 1 or higher"):
            Board(max_row=-1)

    def test_construction_invalid_max_column(self):
        with self.assertRaisesRegex(AssertionError, "Max column must be 1 or higher"):
            Board(max_column=-1)

    def test_set_cell(self):
        row = 1
        column = 1
        self.board.set(row, column)
        self.assertTrue(self.board.get(row, column))
        self.board.set(row, column, False)
        self.assertFalse(self.board.get(row, column))

    def test_str_empty(self):
        expected_board = """------
|    |
|    |
|    |
------"""
        self.assertEqual(expected_board, str(self.board))

    def test_str(self):
        self.board.set(0, 0)
        expected_board = """------
|X   |
|    |
|    |
------"""
        self.assertEqual(expected_board, str(self.board))

    def test_set_glider(self):
        set_glider(0, 0, self.board)
        expected_board = """------
|X   |
| XX |
|XX  |
------"""
        self.assertEqual(expected_board, str(self.board))

    def test_get_living_neighbours_full(self):
        row = 1
        column = 1
        expected_living_neighbours = 0
        for r in range(3):
            for c in range(3):
                self.assertEqual(expected_living_neighbours, self.board.get_living_neighbours(row, column))
                self.board.set(r, c)
                if r != row or c != column:
                    expected_living_neighbours = expected_living_neighbours+1
        self.assertEqual(8, self.board.get_living_neighbours(row, column))


class TestBoardPair(TestCase):

    def setUp(self):
        self.board = BoardPair(3, 4)

    def test_set_cell(self):
        row = 1
        column = 1
        self.assertFalse(self.board.get(row, column))
        self.assertEqual(self.board.get(row, column), self.board.get_active_board().get(row, column))
        self.board.set(row, column)
        self.assertTrue(self.board.get(row, column))
        self.assertEqual(self.board.get(row, column), self.board.get_active_board().get(row, column))

    def test_str(self):
        expected_board = """Active
------
|    |
|    |
|    |
------
Next
------
|    |
|    |
|    |
------"""
        self.assertEqual(expected_board, str(self.board))

    def test_flip(self):
        active_board = self.board.get_active_board()
        next_board = self.board.get_next_board()
        self.board.flip()
        self.assertEqual(next_board, self.board.get_active_board())
        self.assertEqual(active_board, self.board.get_next_board())

