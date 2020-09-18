import logging
import curses
import time
from renderer.base import RendererBase
logger = logging.getLogger(__name__)


class CursesHandler(logging.Handler):
    def __init__(self, screen):
        logging.Handler.__init__(self)
        self.screen = screen

    def emit(self, record):
        try:
            msg = self.format(record)
            screen = self.screen
            fs = "\n%s"
            try:
                screen.addstr(fs % msg)
                screen.refresh()
            except UnicodeError:
                screen.addstr(fs % msg.encode("UTF-8"))
                screen.refresh()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class CursesRenderer(RendererBase):
    def __init__(self, board):
        self.height = board.max_row+2
        self.width = board.max_column+2
        self.screen = curses.initscr()
        self.screen.nodelay(1)
        max_y, max_x = self.screen.getmaxyx()
        self.win = curses.newwin(self.height, self.width)
        self.status_line = curses.newwin(1, max_x, self.height, 0)
        self.logger_win = curses.newwin(max_y - self.height - 3, max_x, self.height+1, 0)
        self.logger_win.scrollok(True)
        self.logger_win.idlok(True)
        self.logger_win.leaveok(True)

    def configure_logging(self, logger_):
        handler = CursesHandler(self.logger_win)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger_.addHandler(handler)

    def draw_header_footer(self, footer=False):
        for c in range(self.width):
            # logger.debug("Drawing column %s" % c)
            try:
                self.win.addch("-")
            except curses.error as err:
                # Writing to bottom right is expected bug in curses
                # https://bugs.python.org/issue8243
                if not (footer and c == self.width - 1):
                    raise

    def draw_board_row(self, board, row):
        for c in range(self.width):
            # logger.debug("Drawing column %s" % c)
            if c == 0 or c == self.width - 1:
                self.win.addch("|")
            else:
                self.win.addch("X" if board.get(row-1, c-1) else " ")

    def draw(self, board, generation):
        self.win.clear()
        try:
            for r in range(self.height):
                logger.debug("Drawing line %s" % r)
                if r == 0 or (r == self.height - 1):
                    self.draw_header_footer(footer=(r == self.height - 1))
                else:
                    self.draw_board_row(board, r)
            self.win.noutrefresh()
            self.set_status("Generation %d" % (generation+1))
            self.update_screen()
            time.sleep(0.2)
        except Exception as err:
            logger.exception(err)

    def set_status(self, status):
        self.status_line.addstr(0, 0, status)
        self.status_line.noutrefresh()

    def update_screen(self):
        self.screen.move(self.height+2, 0)
        curses.doupdate()

