'''
aktualne działanie po uruchomieniu:
symulacja jest zastopowana - należy klikać biały obszar w celu naniesienia punktów początkowych
by rozpocząć symulację należy nacisnąć 's' lub kliknąć myszą dolną część menu, które jest z prawej strony
by zastopować/ nanieść kolejne punky należy nacisnąć klawisz 'p' lub kliknąć myszą górną część menu lub obszar symulacji
'''

import numpy as np
import pygame

#rozmiar tablicy NxM komórek
global N
global M
N=120
M=60

global scale #skala - komórki będą rysowane w rozmiarze scale x scale px
scale=8

#rozmiar pobocznego menu
global N_menu
global M_menu
N_menu=120
M_menu=M*scale

global dead_alive
global neighborhood

neighborhood=np.random.randint(1, size=(N,M))
dead_alive=np.random.randint(1, size=(N,M))

#in progress: aktualnie - kliknięcie górnej części menu - True, dolnej - False - używane przy pauzowaniu symulacji
def stop_button(x,y):
    if (x>N*scale and y<M*scale/2):
        return True
    if (x>N*scale and y>M*scale/2):
        return False

#in progress: rysowanie bocznego menu
def draw_side_menu():
    number_of_buttons=8
    pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(N*scale,0,N_menu,M*scale))
    button_height=M_menu//number_of_buttons
    button_width=N_menu
    #podział menu na ilość guzików równe number_of_buttons - modyfikowalne
    for i in range (0,number_of_buttons):
        pygame.draw.rect(screen, (120, 120, 120+10*i), pygame.Rect(N * scale, i*button_height,button_width, button_height))

#ożyw komórkę o podanych pikselach
def bring_to_life(x,y):
    if (x<N*scale and y<M*scale):
        dead_alive[x//scale][y//scale]=1

#zwróć klikniętą pozycję
def get_position():
    position = pygame.mouse.get_pos()
    return position


#znajduje liczbę sąsiadów punktu (x,y), jeśli x lub y znajduje się na brzegu tablicy o rozmiarze NxM, to sprawdza przeciwległy brzeg tablicy
def find_neighbors(x,y):
    if (x==N-1):
        x3=0
    else:
        x3=x+1
    if (x==0):
        x1=N-1
    else:
        x1=x-1
    if (y==0):
        y1=M-1
    else:
        y1=y-1
    if (y==M-1):
        y3=0
    else:
        y3=y+1
    neighbors=int(dead_alive[x1][y1]+dead_alive[x1][y]+dead_alive[x1][y3]+dead_alive[x][y1]+dead_alive[x][y3]+dead_alive[x3][y1]+dead_alive[x3][y]+dead_alive[x3][y3])
    return neighbors

#zmienia wartość tablicy neighborhood, wyszukuje liczbę sąsiadów dla każdej z komórek
def update_neighborhood():
    for i in range(0,N):
        for j in range(0,M):
            neighborhood[i][j]=find_neighbors(i,j)

#zmiana wartości tablicy martwe-żywe biorąc pod uwagę sąsiadów
def update_dead_alive():
    for i in range (0,N):
        for j in range (0,M):
            if(dead_alive[i][j]==1):
                if(neighborhood[i][j]==2 or neighborhood[i][j]==3):
                    dead_alive[i][j]=1
                else:
                    dead_alive[i][j]=0
            if (dead_alive[i][j]==0):
                if(neighborhood[i][j]==3):
                    dead_alive[i][j]=1
                else:
                    dead_alive[i][j]=0

#wyświetlanie jednego kwadracika podczas pauzy
def display_clicked(x,y):
    x_2=(x//scale)*scale
    y_2=(y//scale)*scale
    if (x_2<N*scale):
        pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(x_2,y_2,scale,scale))

#wyświetlanie tablicy i menu, todo: napisy i guziki w menu
def display_dead_alive():
    for i in range(0, N):
        for j in range(0, M):
            if (dead_alive[i][j] == 1):
                pygame.draw.rect(screen, (0, 0, 0),
                                 pygame.Rect(i * scale, j * scale,scale, scale))
            elif (dead_alive[i][j] == 0):
                pygame.draw.rect(screen, (255, 255, 255),
                                 pygame.Rect(i * scale, j * scale,scale,  scale))
    draw_side_menu()

update_neighborhood()


#właściwości pygame
pygame.init()
SIZE = [(N*scale)+N_menu, M*scale] #dla komórek scale x scale px
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Game of life")

clock = pygame.time.Clock()
done = False
pause = True
display_dead_alive() #pierwsze wyświetlenie pustej tablicy

#pętla programu
while not done:
    screen = pygame.display.get_surface()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            x,y=get_position()
            pause=stop_button(x,y)
            bring_to_life(x,y)
            display_clicked(x,y)
        elif event.type == pygame.KEYDOWN: #pauza możliwa też poprzez przyciski p-pauza s-start
            if event.key == pygame.K_p: pause= True
            if event.key == pygame.K_s: pause= False


    if (pause == False):
        display_dead_alive()
        update_neighborhood()
        update_dead_alive()
        pygame.time.wait(100)
    pygame.display.flip()

    clock.tick(20)

pygame.quit()


'''
pomysły i rzeczy do zrobienia:
-wybór i stworzenie interaktywnych, podpisanych guzików
-wczytywanie struktur z pliku
-możliwość symulacji krok po kroku - jedna generacja co kliknięcie
-licznik generacji
-przybliżanie-oddalanie
-przyspieszanie/spowalnianie automatycznej symulacji
-możliwość modyfikacji reguł (zamaist Conwaya 2,3-przeżywa, 3-ożywa jakieś inne do wyboru, np 4,5,6-przeżywa, 3,4 ożywa itp)
-menu główne - opis zasad, struktur, start

-optymalizacja przeszukiwania/wyświetlania - śledzenie nieaktywnych obszarów i ignorowanie ich
-refaktoryzacja kodu, rozłożenie na pliki
-optymalizacja funkcji - zamiana sztywnych danych na zmienne, rozbicie na funkcje co się da
-?????

-symulowanie bardzo dużej tablicy - np dodanie suwaków by poruszać się po planszy
-rozpocxęcie od losowych wartości komórek - wylosowanie tablicy martwe/żywe

-znalezienie dodatkowych źródeł naukowych, poprawa wstępu teoretycznego

do przemyślenia:
-zmiana podejścia dot. implementacji nieskończonej planszy ewentualnie sposobu jej wyświetlania
-dodatkowe opcje
'''
