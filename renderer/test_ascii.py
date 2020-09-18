from unittest import TestCase
from renderer.ascii import Renderer
from board import Board


class TestRenderer(TestCase):
    def setUp(self):
        self.renderer = Renderer()
        self.board = Board(max_row=2, max_column=3)

    def test_draw_empty_board(self):
        expected_board = """-----
|   |
|   |
-----"""
        self.assertEqual(expected_board, self.renderer.draw(self.board))

    def test_draw_board(self):
        self.board.set(0, 0)
        expected_board = """-----
|X  |
|   |
-----"""
        self.assertEqual(expected_board, self.renderer.draw(self.board))
