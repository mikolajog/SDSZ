import pygame
import pygame.locals
from constants import *
from button import Button

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
        self.surface = pygame.display.set_mode((width+200, height), 0, 32)
        pygame.display.set_caption('Game of life')


        self.height = height
        self.width = width

        self.start_button = Button(160, 50, self.width + 20, self.height * 0.2, 3, self.surface, RED, "Start")
        self.pause_button = Button(160, 50, self.width + 20, self.height * 0.5, 3, self.surface, RED, "Pause")
        self.end_button = Button(160, 50, self.width + 20, self.height * 0.8, 3, self.surface, RED, "End")




    def draw(self, *args):
        """
        Draws the window for the game

        :param args: list of object to draw
        """

        # setting black background
        self.surface.fill(BLACK)

        pygame.draw.line(self.surface, RED, (self.width, 0), (self.width, self.height), 3)


        self.start_button.draw()
        self.pause_button.draw()
        self.end_button.draw()

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('MENU', True, GREEN)
        textRect = text.get_rect()
        textRect.center = (self.width+100, self.height*0.05)
        self.surface.blit(text, textRect)

        for drawable in args:
            drawable.draw_on(self.surface)


        #updating the display and making visible changes on the screen
        pygame.display.update()

