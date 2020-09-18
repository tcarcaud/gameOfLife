import logging
from PIL import Image, ImageDraw, ImageFont
from renderer.base import RendererBase
logger = logging.getLogger(__name__)

GRID_SIZE = 10


class GifRenderer(RendererBase):
    def __init__(self, board):
        self.frames = list()
        self.current_frame = None
        self.height = board.max_row + 1
        self.width = board.max_column

    def configure_logging(self, logger_):
        logging.basicConfig()

    def draw_board_row(self, board, r):
        for c in range(board.max_column):
            if board.get(r, c):
                square = (c*GRID_SIZE, (r+1)*GRID_SIZE, (c+1)*GRID_SIZE, (r+2)*GRID_SIZE)
                logger.debug("Drawing square %s" % str(square))
                self.current_frame.rectangle(square, fill='Black')

    def draw(self, board, generation):
        image = Image.new('RGB', (self.width*GRID_SIZE, self.height*GRID_SIZE), (255, 255, 255))
        self.current_frame = ImageDraw.Draw(image)
        for r in range(self.height):
            logger.debug("Drawing row %s" % r)
            if r == 0:
                fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 10)
                self.current_frame.text((0, 0), "Generation {:}".format(generation), font=fnt, fill='Black')
            else:
                self.draw_board_row(board, r-1)
        self.frames.append(image)

    def finish(self):
        self.save_as_image('glider.gif')

    def save_as_image(self, filename):
        logging.info("Saving %d frames to %s" % (len(self.frames), filename))
        self.frames[0].save(filename, format='GIF',
                            append_images=self.frames[1:],
                            save_all=True,
                            duration=80, loop=0)

