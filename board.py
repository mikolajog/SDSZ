import pygame
import pygame.locals
import constants
from constants import *
from button import Button

class Board(object):
    """
    Game board responsible for:
    providing window (__init__)
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

        #Prepares buttons for menu
        self.start_button = Button(160, 50, self.width + 20, self.height * 0.2, 3, self.surface, TURQUOISE, "Start")
        self.pause_button = Button(160, 50, self.width + 20, self.height * 0.35, 3, self.surface, TURQUOISE, "Pause")
        self.next_button = Button(160, 50, self.width + 20, self.height * 0.5, 3, self.surface, TURQUOISE, "Next")
        self.slow_button = Button(75, 50, self.width + 20, self.height * 0.65, 3, self.surface, TURQUOISE, ">")
        self.speed_button = Button(75, 50, self.width + 105, self.height * 0.65, 3, self.surface, TURQUOISE, ">>")
        self.end_button = Button(160, 50, self.width + 20, self.height * 0.8, 3, self.surface, TURQUOISE, "End")



    def draw(self, *args):
        """
        Draws the window and menu for the game

        :param args: list of object to draw
        """

        # setting black background
        self.surface.fill(BLACK)

        #Menu

        #Vertical line
        pygame.draw.line(self.surface, TURQUOISE, (self.width, 0), (self.width, self.height), 3)

        #Buttons
        self.start_button.draw()
        self.pause_button.draw()
        self.next_button.draw()
        self.slow_button.draw()
        self.speed_button.draw()
        self.end_button.draw()

        #Menu text
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('MENU', True, BLUE)
        textRect = text.get_rect()
        textRect.center = (self.width+100, self.height*0.05)
        self.surface.blit(text, textRect)

        #Generations count
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render("Generations: "+str(constants.number_of_generations), True, DARK_RED)
        textRect = text.get_rect()
        textRect.center = (self.width + 100, self.height * 0.12)
        self.surface.blit(text, textRect)

        #Time display
        text = font.render("Time: " + str(round(constants.time_in_seconds,2)) + "s", True, DARK_RED)
        textRect = text.get_rect()
        textRect.center = (self.width + 100, self.height * 0.16)
        self.surface.blit(text, textRect)

        # Delay display
        text = font.render("Slowed down by: " + str(constants.delay) + "ms", True, DARK_RED)
        textRect = text.get_rect()
        textRect.center = (self.width + 100, self.height * 0.96)
        self.surface.blit(text, textRect)

        #draws population on the surface
        for drawable in args:
            drawable.draw_on(self.surface)


        #updating the display and making visible changes on the screen
        pygame.display.update()

