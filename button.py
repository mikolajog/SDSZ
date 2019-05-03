import pygame

class Button(object):
    """
    We create Button with provided text, color, position and size
    Button has methods:
    draw() which draws button on given surface
    is_clicked() returns True when button is clicked
    """
    def __init__(self, size_x, size_y, position_x, position_y, thickness, surface, color, tekst):
        self.size_x = size_x
        self.size_y = size_y
        self.position_x = position_x
        self.position_y = position_y
        self.thickness = thickness
        self.surface = surface
        self.color = color
        self.tekst = tekst

    def draw(self):
        pygame.draw.rect(self.surface, self.color, pygame.locals.Rect((self.position_x, self.position_y), (self.size_x, self.size_y)), self.thickness)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(self.tekst, True, self.color)
        textRect = text.get_rect()
        textRect.center = (self.position_x+(self.size_x*0.5), self.position_y+(self.size_y*0.5))
        self.surface.blit(text, textRect)

    def is_clicked(self):
        """
        :return: True when button is clicked
        """
        # pobierz stan guzików myszki z wykorzystaniem funcji pygame
        buttons = pygame.mouse.get_pressed()
        if not any(buttons):
            # ignoruj zdarzenie jeśli żaden z guzików nie jest wciśnięty
            return

        # pobierz pozycję kursora na mierzoną w pikselach
        x, y = pygame.mouse.get_pos()

        if (x >= self.position_x and x<= self.position_x+self.size_x and y>=self.position_y and y<=self.position_y+self.size_y):
            return True
