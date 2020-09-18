from renderer.ascii import TextRenderer
from renderer.console import CursesRenderer
from renderer.image import GifRenderer


def create_renderer(renderer_type, board):
    if renderer_type == 'ascii':
        return TextRenderer()
    elif renderer_type == 'console':
        return CursesRenderer(board)
    elif renderer_type == 'image':
        return GifRenderer(board)
    else:
        raise Exception('Renderer type "{:}" unknown'.format(renderer_type))