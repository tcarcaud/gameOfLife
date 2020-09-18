class Renderer:
    def draw(self, board):
        result = "-{:}-\n".format("-"*board.max_column)
        for r in range(board.max_row):
            result += "|"
            for c in range(board.max_column):
                result += "X" if board.get(r, c) else " "
            result += "|\n"
        result += "-{:}-".format("-"*board.max_column)
        return result

