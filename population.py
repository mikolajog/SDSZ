import pygame

from constants import DEAD, ALIVE

class Population(object):
    """
    Populacja komórek
    """

    def __init__(self, width, height, cell_size=10):
        """
        Przygotowuje ustawienia populacji

        :param width: szerokość planszy mierzona liczbą komórek
        :param height: wysokość planszy mierzona liczbą komórek
        :param cell_size: bok komórki w pikselach
        """
        self.box_size = cell_size
        self.height = height
        self.width = width
        self.generation = self.reset_generation()

    def reset_generation(self):
        return [[DEAD for y in range(self.height)] for x in range(self.width)]

    def handle_mouse(self):
        # pobierz stan guzików myszki z wykorzystaniem funcji pygame
        buttons = pygame.mouse.get_pressed()
        if not any(buttons):
            # ignoruj zdarzenie jeśli żaden z guzików nie jest wciśnięty
            return

        # dodaj żywą komórką jeśli wciśnięty jest pierwszy guzik myszki
        # będziemy mogli nie tylko dodawać żywe komórki ale także je usuwać
        alive = True if buttons[0] else False

        # pobierz pozycję kursora na planszy mierzoną w pikselach
        x, y = pygame.mouse.get_pos()

        # przeliczamy współrzędne komórki z pikseli na współrzędne komórki w macierz
        # gracz może kliknąć w kwadracie o szerokości box_size by wybrać komórkę
        x /= self.box_size
        y /= self.box_size

        # ustaw stan komórki na macierzy
        self.generation[int(x)][int(y)] = ALIVE if alive else DEAD

    def draw_on(self, surface):
        """
        Rysuje komórki na planszy
        """
        for x, y in self.alive_cells():
            size = (self.box_size, self.box_size)
            position = (x * self.box_size, y * self.box_size)
            color = (255, 255, 255)
            thickness = 1
            pygame.draw.rect(surface, color, pygame.locals.Rect(position, size), thickness)

    def alive_cells(self):
        """
        Generator zwracający współrzędne żywych komórek.
        """
        for x in range(len(self.generation)):
            column = self.generation[x]
            for y in range(len(column)):
                if column[y] == ALIVE:
                    # jeśli komórka jest żywa zwrócimy jej współrzędne
                    yield x, y

    def neighbours(self, x, y):
        """
        Generator zwracający wszystkich okolicznych sąsiadów
        """
        for nx in range(x - 1, x + 2):
            for ny in range(y - 1, y + 2):
                if nx == x and ny == y:
                    # pomiń współrzędne centrum
                    continue
                if nx >= self.width:
                    # sąsiad poza końcem planszy, bierzemy pierwszego w danym rzędzie
                    nx = 0
                elif nx < 0:
                    # sąsiad przed początkiem planszy, bierzemy ostatniego w danym rzędzie
                    nx = self.width - 1
                if ny >= self.height:
                    # sąsiad poza końcem planszy, bierzemy pierwszego w danej kolumnie
                    ny = 0
                elif ny < 0:
                    # sąsiad przed początkiem planszy, bierzemy ostatniego w danej kolumnie
                    ny = self.height - 1

                # dla każdego nie pominiętego powyżej
                # przejścia pętli zwróć komórkę w tych współrzędnych
                yield self.generation[nx][ny]

    def cycle_generation(self):
        """
        Generuje następną generację populacji komórek
        """
        next_gen = self.reset_generation()
        for x in range(len(self.generation)):
            column = self.generation[x]
            for y in range(len(column)):
                # pobieramy wartości sąsiadów
                # dla żywej komórki dostaniemy wartość 1 (ALIVE)
                # dla martwej otrzymamy wartość 0 (DEAD)
                # zwykła suma pozwala nam określić liczbę żywych sąsiadów
                count = sum(self.neighbours(x, y))
                if count == 3:
                    # rozmnażamy się
                    next_gen[x][y] = ALIVE
                elif count == 2:
                    # przechodzi do kolejnej generacji bez zmian
                    next_gen[x][y] = column[y]
                else:
                    # za dużo lub za mało sąsiadów by przeżyć
                    next_gen[x][y] = DEAD

        # nowa generacja staje się aktualną generacją
        self.generation = next_gen