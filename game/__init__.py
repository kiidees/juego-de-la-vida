import pygame, sys
import numpy as np
import time
from pygame.locals import *
import pygame.mixer

pygame.init()
# ancho y alto de la pantalla.
width, height = 750, 750
# creacion de la pantalla.
screen = pygame.display.set_mode((height, width))
# color del fondo
bg = 25, 25, 25
# rellenar el fondo
screen.fill(bg)
nXc, nYc = 100, 100
dimCw = width / nXc
dimCh = height / nYc
# Estado de las celdas
gameStatus = np.zeros((nXc, nYc))

# automata palo


gameStatus[5, 3] = 1
gameStatus[5, 4] = 1
gameStatus[5, 5] = 1

# automata en movimiento
gameStatus[21, 21] = 1
gameStatus[22, 22] = 1
gameStatus[22, 23] = 1
gameStatus[21, 23] = 1
gameStatus[20, 23] = 1

pauseExecution = False


# ejecucion infinita
while True:

    pygame.event.get()
    newGameStatus = np.copy(gameStatus)
    screen.fill(bg)
    #time.sleep(0.001)
    time.sleep(0.001)

    # eventos del teclado
    #ev = pygame.event.get()


    mouseClick = pygame.mouse.get_pressed()
    # print(mouseClick)
    if sum(mouseClick) > 0:
        posX, posY = pygame.mouse.get_pos()
        celX, celY = int(np.floor(posX / dimCw)), int(np.floor(posY / dimCh))
        newGameStatus[celX, celY] = not mouseClick[2]
    for y in range(0, nXc):
        for x in range(0, nYc):

            if not pauseExecution:
                # numero de vecinos
                n_neighbours = gameStatus[(x - 1) % nXc, (y - 1) % nYc] + \
                               gameStatus[(x) % nXc, (y - 1) % nYc] + \
                               gameStatus[(x + 1) % nXc, (y - 1) % nYc] + \
                               gameStatus[(x - 1) % nXc, (y) % nYc] + \
                               gameStatus[(x + 1) % nXc, (y) % nYc] + \
                               gameStatus[(x - 1) % nXc, (y + 1) % nYc] + \
                               gameStatus[(x) % nXc, (y + 1) % nYc] + \
                               gameStatus[(x + 1) % nXc, (y + 1) % nYc]
                # regla 1 celula muerta con 3 cevinos vimos va a revivir
                if gameStatus[x, y] == 0 and n_neighbours == 3:
                    newGameStatus[x, y] = 1
                # regla 2 celula con menos de dos o mas de 3 muere
                elif gameStatus[x, y] == 1 and (n_neighbours < 2 or n_neighbours > 3):
                    newGameStatus[x, y] = 0
                    pygame.mixer.music.load('xplo8bit.mp3')
                    pygame.mixer.music.play()
            polyg = [((x) * dimCw, y * dimCh),
                     ((x + 1) * dimCw, y * dimCh),
                     ((x + 1) * dimCw, (y + 1) * dimCh),
                     ((x) * dimCw, (y + 1) * dimCh)]
            # coloreamos la celda para cada par de x e y
            if newGameStatus[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), polyg, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), polyg, 0)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pauseExecution = not pauseExecution
    gameStatus = np.copy(newGameStatus)
    pygame.display.flip()
pass