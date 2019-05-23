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
        self.start_button = Button(160, 35, self.width + 20, self.height * 0.20, 2, self.surface, TURQUOISE, "Start",32)
        self.pause_button = Button(160, 35, self.width + 20, self.height * 0.30, 2, self.surface, TURQUOISE, "Pause",32)
        self.next_button = Button(160, 35, self.width + 20, self.height * 0.40, 2, self.surface, TURQUOISE, "Next",32)
        self.slow_button = Button(75, 35, self.width + 20, self.height * 0.50, 2, self.surface, TURQUOISE, ">",32)
        self.speed_button = Button(75, 35, self.width + 105, self.height * 0.50, 2, self.surface, TURQUOISE, ">>",32)
        self.load_button = Button(75, 35, self.width + 20, self.height * 0.60, 2, self.surface, TURQUOISE, "Load",20)
        self.save_button = Button(75, 35, self.width + 105, self.height * 0.60, 2, self.surface, TURQUOISE, "Save",20)
        self.end_button = Button(160, 35, self.width + 20, self.height * 0.70, 2, self.surface, TURQUOISE, "End",32)
        self.info_button = Button(160, 35, self.width + 20, self.height * 0.80, 2, self.surface, TURQUOISE, "Info", 32)



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
        self.load_button.draw()
        self.save_button.draw()
        self.end_button.draw()
        self.info_button.draw()

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

