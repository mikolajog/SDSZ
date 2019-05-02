import pygame

class Board(object):
    """
    Game board responsible for:
    providing window(__init__)
    drawing(draw)

    """

    def __init__(self, width, height):
        """
        Constructor for board.
        Prepares window for the game.

        :param width: width in pixels
        :param height: height in pixels

        """
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption('Game of life')

    def draw(self, *args):
        """
        Draws the window for the game

        :param args: list of object to draw
        """

        # seting black background
        background = (0, 0, 0)
        self.surface.fill(background)

        for drawable in args:
            drawable.draw_on(self.surface)

        #updating the display and making visible changes on the screen
        pygame.display.update()