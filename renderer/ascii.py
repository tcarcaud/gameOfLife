from renderer.base import RendererBase


class TextRenderer(RendererBase):
    def draw_board(self, board):
        result = "-{:}-\n".format("-"*board.max_column)
        for r in range(board.max_row):
            result += "|"
            for c in range(board.max_column):
                result += "X" if board.get(r, c) else " "
            result += "|\n"
        result += "-{:}-".format("-"*board.max_column)
        return result

    def draw(self, board, generation=None):
        print(self.draw_board(board))

