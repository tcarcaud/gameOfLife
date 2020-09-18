def next_state(row, column, board):
    living_neighbours = board.get_living_neighbours(row, column)
    if board.get(row, column):
        return living_neighbours == 2 or living_neighbours == 3
    else:
        return living_neighbours == 3


def next_board(board, next_board_):
    for row in range(board.max_row):
        for column in range(board.max_column):
            next_board_.set(row, column, next_state(row, column, board))
