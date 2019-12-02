import pygame
from pygame.locals import *
from Rikishi import Rikishi
from Circle import Circle
from Position import Position2D
from Directions import Directions as Dirs

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def turnOnOffPin(pin, on):
    GPIO.setup(pin, GPIO.OUT)
    if on:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)

def simulateClick(pin)
    turnOnOffPin(pin, False)
    time.sleep(0.01)
    turnOnOffPin(pin, True)

pins = [ 17, 18, 27 ]
for pin in pins
    turnOnOffPin(pin, True)

def blinkLedsSequence():
    simulateClick(pins[0])

def blinkLedsEvenOdd():
    simulateClick(pins[1])

def blinkLeds():
    simulateClick(pins[2])

pygame.init()
screen = pygame.display.set_mode((400, 300))
centro = Position2D(x=200,y=150)
raio = 150

clock = pygame.time.Clock()

riki1 = Rikishi(pos = Position2D(170, 70))
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

        #segundo player
        if pressed [K_w]:
            riki1.accelToward(Dirs.UP)
        elif pressed [K_s]:
            riki1.accelToward(Dirs.DOWN)
        else:
            riki1.stopAccelToward(Dirs.DOWN)

        if pressed [K_a]:
            riki1.accelToward(Dirs.LEFT)
        elif pressed [K_d]:
            riki1.accelToward(Dirs.RIGHT)
        else:
            riki1.stopAccelToward(Dirs.LEFT)

    #Processing
    if(riki1.hasCollision(riki2)):
        riki1.transferMomentum(riki2)
        riki2.transferMomentum(riki1)

    if(centro.distance(riki1.Centre)> raio):
        print("2 ganhou")

        for i in range(30):
            blinkLedsSequence()
            if(i%2 == 1):
                blinkLedsEvenOdd()
            if(i%3 == 0):
                blinkLeds()

        exit()

    if(centro.distance(riki2.Centre)> raio):
        print("1 ganhou")

        for i in range(30):
            blinkLeds()
            if(i%2 == 1):
                blinkLedsSequence()
            if(i%3 == 0):
                blinkLedsEvenOdd()

        exit()



    riki1.process()
    riki2.process()

    #Rendering
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (0,0,255), centro.toTuple(), raio, 2)
    riki1.render(screen)
    riki2.render(screen)
    pygame.display.flip()
