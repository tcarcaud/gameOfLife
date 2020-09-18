import random
import logging
from board import BoardPair, set_glider, set_random
from controller import next_board
from renderer import create_renderer
logger = logging.getLogger()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Play Conway's game of life on 2D board.", fromfile_prefix_chars='@')
    parser.add_argument('--render', choices=['ascii', 'console', 'image'], default='console',
                        help='How the board is displayed')
    parser.add_argument('--width', type=int, default=10,
                        help='Board width in cells')
    parser.add_argument('--height', type=int, default=9,
                        help='Board height in cells')
    parser.add_argument('--generation', type=int, default=60,
                        help='Number of generation to play')
    args = parser.parse_args()

    board = BoardPair(args.height, args.width)
    renderer = create_renderer(args.render, board)
    renderer.configure_logging(logger)
    logger.setLevel(level=logging.INFO)

#    set_glider(0, 0, board)
#    random.seed(42)
    set_random(board)
    for generation in range(args.generation):
        renderer.draw(board, generation)
        next_board(board.get_active_board(), board.get_next_board())
        board.flip()

    renderer.finish()

