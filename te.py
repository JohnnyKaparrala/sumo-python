import pygame
from pygame.locals import *
from Rikishi import Rikishi
from Position import Position2D
from Directions import Directions as Dirs

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

riki1 = Rikishi(pos = Position2D(170, 20))
riki2 = Rikishi(pos = Position2D(170, 280))

while True:
    clock.tick(30)

    #Events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        pressed = pygame.key.get_pressed()
        if pressed [K_UP]:
            riki2.accelToward(Dirs.UP)
        elif pressed [K_DOWN]:
            riki2.accelToward(Dirs.DOWN)
        else:
            riki2.stopAccelToward(Dirs.DOWN)

        if pressed [K_LEFT]:
            riki2.accelToward(Dirs.LEFT)
        elif pressed [K_RIGHT]:
            riki2.accelToward(Dirs.RIGHT)
        else:
            riki2.stopAccelToward(Dirs.LEFT)

    #Processing
    if(riki1.hasCollision(riki2)):
        riki1.transferMomentum(riki2)
        riki2.transferMomentum(riki1)

    riki1.process()
    riki2.process()

    #Rendering
    screen.fill((0, 0, 0))
    riki1.render(screen)
    riki2.render(screen)
    pygame.display.flip()
