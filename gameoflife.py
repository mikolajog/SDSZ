# coding=utf-8

import pygame
import pygame.locals
import constants
import time
import shelve
import os
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN
from board import Board
from population import Population
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename


class GameOfLife(object):

    """
    Puts together all parts of the game.
    """

    def __init__(self, width, height, cell_size=10):
        """
        Settings for the game
        :param width: width measured by number of cells
        :param height: height measured by number of cells
        :param cell_size: size of the cell
        """
        pygame.init()

        self.board = Board(width * cell_size, height * cell_size)

        #Clock responsible for frequency of drawing cells
        self.fps_clock = pygame.time.Clock()

        self.population = Population(width, height, cell_size)

        #To define whether the game has started or not
        self.started = False

    def run(self):
        """
        Main loop
        """
        while not self.handle_events():

            self.board.draw(self.population)
            if self.started:
                self.population.cycle_generation()
                pygame.time.delay(constants.delay)
            self.fps_clock.tick(15)


    def handle_events(self):
        """
        Function responsible for handling events in game
        for example mouse clicks

        :return True if the game should end
        """
        if (self.started==True):
            constants.running_time=time.time()-constants.start_time
            constants.already_running=True
            constants.time_in_seconds=constants.running_time
        elif (self.started==False and constants.already_running==True):
            constants.negative_time = time.time() - constants.pause_time


        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                return True

            if event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN:
                if self.board.start_button.is_clicked():

                    if (self.started == False and constants.already_running == False):
                        constants.start_time = time.time()
                    constants.start_time += constants.negative_time
                    constants.negative_time = 0
                    constants.time_in_seconds = constants.running_time
                    self.started = True
                    constants.already_running = True
                    constants.step_running=False



                elif self.board.pause_button.is_clicked():
                    if (constants.already_running == True and constants.step_running==False):
                        constants.pause_time = time.time()
                    self.started = False

                elif self.board.next_button.is_clicked():
                    if (constants.step_running==False):
                        constants.pause_time = time.time()
                    constants.step_running=True
                    self.started = False
                    self.population.cycle_generation()

                elif self.board.slow_button.is_clicked():
                        constants.delay+=50

                elif self.board.speed_button.is_clicked():
                    if (constants.delay>0):
                        constants.delay-=50

                elif self.board.end_button.is_clicked():
                    self.population.generation = self.population.reset_generation()
                    self.population.cycle_generation()
                    self.started = False
                    constants.number_of_generations = 0
                    constants.time_in_seconds = 0
                    constants.negative_time = 0
                    constants.already_running = False
                elif self.board.save_button.is_clicked():
                    root = Tk()
                    root.withdraw()
                    root.attributes("-topmost", True)
                    fullpath = asksaveasfilename()  # show an "Open" dialog box and return the path to the selected file
                    if (not fullpath):
                        break
                    number = fullpath.rfind('/')
                    path = fullpath[:number]
                    filename = fullpath[number + 1:]
                    if(fullpath[-4:]==".dir"):
                        filename = fullpath[number + 1:-4]
                    elif(fullpath.rfind(".")==-1):
                        filename = fullpath[number + 1:]
                    else:
                        break
                    curr = os.getcwd()
                    os.chdir(path)
                    shelfFile = shelve.open(filename)
                    shelfFile['constants.delay'] =constants.delay
                    shelfFile['constants.time_in_seconds'] =constants.time_in_seconds
                    shelfFile['constants.number_of_generations'] = constants.number_of_generations
                    shelfFile['population.box_size'] = self.population.box_size
                    shelfFile['population.height'] = self.population.height
                    shelfFile['population.width'] = self.population.width
                    shelfFile['population.generation'] = self.population.generation
                    shelfFile.close()
                    os.chdir(curr)

                elif self.board.load_button.is_clicked():
                    root = Tk()
                    root.withdraw()
                    root.attributes("-topmost", True)
                    fullpath = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
                    if(not fullpath):
                        break
                    number = fullpath.rfind('/')
                    path = fullpath[:number]
                    filename = fullpath[number + 1:]
                    if (fullpath[-4:] == ".dir"):
                        filename = fullpath[number + 1:-4]
                    elif (fullpath.rfind(".") == -1):
                        filename = fullpath[number + 1:]
                    else:
                        break
                    curr = os.getcwd()
                    os.chdir(path)
                    shelfFile = shelve.open(filename)
                    self.started = False
                    constants.number_of_generations = 0
                    constants.time_in_seconds = 0
                    constants.negative_time = 0
                    constants.already_running = False
                    constants.delay=shelfFile['constants.delay']
                    constants.time_in_seconds = shelfFile['constants.time_in_seconds']
                    constants.number_of_generations = shelfFile['constants.number_of_generations']
                    self.population.box_size = shelfFile['population.box_size']
                    self.population.height = shelfFile['population.height']
                    self.population.width = shelfFile['population.width']
                    self.population.generation = shelfFile['population.generation']
                    shelfFile.close()
                    os.chdir(curr)
                else:
                    self.population.handle_mouse()
        return False




