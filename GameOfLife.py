import pygame
import time, os
import numpy as np

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()

pygame.display.set_caption("Juego de la vida - Chamex")

iconPath = "./icon.ico"

if os.path.exists(iconPath):
    
    icono = pygame.image.load(iconPath)

    pygame.display.set_icon(icono)

width, height = 1000, 1000

screen = pygame.display.set_mode((height,width))

bg = 25, 25, 25

screen.fill(bg)

nxC, nyC = 60, 60  

dimCW = width / nxC
dimCH = height / nyC

gameState = np.zeros((nxC, nyC))

# # automata palo

# gameState[5,3] = 1
# gameState[5,3] = 1
# gameState[5,3] = 1

# # automata movil

# gameState[21, 21] = 1
# gameState[22, 22] = 1
# gameState[22, 23] = 1
# gameState[21, 23] = 1
# gameState[20, 23] = 1

posInitX = int((nxC / 2) - 3)
posInitY = int((nyC / 2) - 5)
gameState[posInitX, posInitY] = 1
gameState[posInitX + 1, posInitY] = 1
gameState[posInitX + 2, posInitY] = 1
gameState[posInitX + 3, posInitY] = 1

gameState[posInitX + 3, posInitY + 1] = 1
gameState[posInitX + 3, posInitY + 2] = 1

gameState[posInitX, posInitY + 3] = 1
gameState[posInitX + 3, posInitY + 3] = 1

gameState[posInitX, posInitY + 4] = 1
gameState[posInitX + 1, posInitY + 4] = 1
gameState[posInitX + 2, posInitY + 4] = 1
gameState[posInitX + 3, posInitY + 4] = 1

pauseExect = True

endGame = False

interation = 0


while not endGame:

    newGameState = np.copy(gameState) 

    screen.fill(bg)

    time.sleep(0.1)

    ev = pygame.event.get()

    population = 0

    for event in ev:

        if event.type == pygame.QUIT:
            endGame = True
            break

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                endGame = True
                break

            if event.key == pygame.K_r:
                interation = 0
                gameState = np.zeros((nxC, nyC))
                newGameState = np.zeros((nxC, nyC))
                pauseExect = True
            else:
                pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()
        
        if sum(mouseClick) > 0:

            if mouseClick[1]:

                pauseExect = not pauseExect
            else:
                posX, posY = pygame.mouse.get_pos()
                celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
                newGameState[celX, celY] = not mouseClick[2]
    
    if not pauseExect:
        interation += 1

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:

                n_neigh = (
                    gameState[(x - 1) % nxC, (y - 1) % nyC]
                    + gameState[x % nxC, (y - 1) % nyC]
                    + gameState[(x + 1) % nxC, (y - 1) % nyC]
                    + gameState[(x - 1) % nxC, y % nyC]
                    + gameState[(x + 1) % nxC, y % nyC]
                    + gameState[(x - 1) % nxC, (y + 1) % nyC]
                    + gameState[x % nxC, (y + 1) % nyC]
                    + gameState[(x + 1) % nxC, (y + 1) % nyC]
                )

                if gameState[x , y] == 0 and n_neigh == 3:
                    newGameState[x , y] = 1

                if gameState[x , y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x,y] = 0
            
            if gameState[x,y] == 1:
                population += 1

            poly = [
                (int(x * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int((y + 1) * dimCH)),
                (int(x * dimCW), int((y + 1) * dimCH)),
            ]

            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                if pauseExect:
                    pygame.draw.polygon(screen, (128,128,128), poly, 0)
                else:
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    title = f"Juego de la Vida - Chamex - Poblacion: {population} - Generation: {interation}"

    if pauseExect:
        title += "- [PAUSADO]"
    
    pygame.display.set_caption(title)
    print(title)

    gameState = np.copy(newGameState)

    pygame.display.flip()

print("Juego Finalizado - Chamex")