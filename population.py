import pygame

from constants import *

class Population(object):
    """
    Population of cells
    """

    def __init__(self, width, height, cell_size=10):
        """
        Prepares population settings

        :param width: width measured by number of cells
        :param height: height measured by number of cells
        :param cell_size: size of the cell
        """
        self.box_size = cell_size
        self.height = height
        self.width = width
        self.generation = self.reset_generation()

    def reset_generation(self):
        return [[DEAD for _ in range(self.height)] for _ in range(self.width)]

    def handle_mouse(self):
        # get mouse buttons state
        buttons = pygame.mouse.get_pressed()
        if not any(buttons):
            # ignore event when none of buttons is pressed
            return

        #if we click left button we add cells otherwise we delete them
        alive = True if buttons[0] else False

        # get mouse position measured in pixels
        x, y = pygame.mouse.get_pos()

        #to check if its within game board size
        if(x>self.width*self.box_size):
            return

        #counting coordinates of cells from pixels to matrix
        x /= self.box_size
        y /= self.box_size

        #setting cells states on matrix
        self.generation[int(x)][int(y)] = ALIVE if alive else DEAD

    def draw_on(self, surface):
        """
        Draws cells on given surface
        """
        for x, y in self.alive_cells():
            #size = (self.box_size, self.box_size)
            #position = (x * self.box_size, y * self.box_size)
            #thickness = 1
            pygame.draw.rect(surface, PINK, (x * self.box_size, y * self.box_size,self.box_size, self.box_size ))

    def alive_cells(self):
        """
        :return list of tuples with coordinates of alive cells
        """
        list=[]

        for x in range(len(self.generation)):
            column = self.generation[x]
            for y in range(len(column)):
                if column[y] == ALIVE:
                    # append if cell is alive
                    list.append((x, y))

        return list

    def neighbours(self, x, y):
        """
        :return list of neighbours for cell with given x,y
        """

        neighbours=[]
        for nx in range(x - 1, x + 2):
            for ny in range(y - 1, y + 2):
                if nx == x and ny == y:
                    # skip when it's me
                    continue
                if nx >= self.width:
                    #neighbour is further than end -> we take first in row
                    nx = 0
                elif nx < 0:
                    #neighbour before the beginning -> we take last in row
                    nx = self.width - 1
                if ny >= self.height:
                    # neighbour is further than end -> we take first in column
                    ny = 0
                elif ny < 0:
                    # neighbour before the beginning -> we take last in column
                    ny = self.height - 1

                #for any other:
                neighbours.append(self.generation[nx][ny])

        return neighbours

    def cycle_generation(self):
        """
        :return next generation of alive cells
        """
        next_gen = self.reset_generation()
        for x in range(len(self.generation)):
            column = self.generation[x]
            for y in range(len(column)):
                #sum neighbours(ALIVE has value 1, DEAD has 0)
                count = sum(self.neighbours(x, y))
                if count == 3:
                    #We are ALIVE now
                    next_gen[x][y] = ALIVE
                elif count == 2:
                    #Its the same
                    next_gen[x][y] = column[y]
                else:
                    #Not enough neighbours -> DEAD
                    next_gen[x][y] = DEAD

        #Next generation becomes "old" generation
        self.generation = next_gen