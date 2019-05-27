import pygame

class Button(object):
    """
    Creates Button with provided text, color, position and size
    """
    def __init__(self, size_x, size_y, position_x, position_y, thickness, surface, color, tekst, font_size):
        self.size_x = size_x
        self.size_y = size_y
        self.position_x = position_x
        self.position_y = position_y
        self.thickness = thickness
        self.surface = surface
        self.color = color
        self.tekst = tekst
        self.font_size = font_size

    def draw(self):
        """
        Draws button on given surface
        """
        #draw button's frame
        pygame.draw.rect(self.surface, self.color, pygame.locals.Rect((self.position_x, self.position_y), (self.size_x, self.size_y)), self.thickness)

        #writes text on the button
        font = pygame.font.Font('freesansbold.ttf', self.font_size)
        text = font.render(self.tekst, True, self.color)
        textRect = text.get_rect()
        textRect.center = (self.position_x+(self.size_x*0.5), self.position_y+(self.size_y*0.5))
        self.surface.blit(text, textRect)

    def is_clicked(self):
        """
        :return: True when button is clicked
        """
        #get mouse buttons state
        buttons = pygame.mouse.get_pressed()
        if not any(buttons):
            #ignore event when none of buttons is pressed
            return
        #get mouse position measured in pixels
        x, y = pygame.mouse.get_pos()

        #check if mouse position is within borders of button
        if (x >= self.position_x and x<= self.position_x+self.size_x and y>=self.position_y and y<=self.position_y+self.size_y):
            return True
