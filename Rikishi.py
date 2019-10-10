from Directions import Directions as Direc
from Acceleration import Acceleration2D, Speed2D
import pygame

class Rikishi(Circle):
    
    def __init__(self,
                 pos=Position2D(0,0),
                 r=20, #radius in pixels
                 color = (155, 0, 0)
    ):
        self.Centre = pos                 #(pixel, pixel)
        self.Radius = Radius              #pixel
        self.Speed  = Speed2D(0,0)        #pixel/update
        self.Accel  = Acceleration2D(0,0) #pixel/update**2
        self.Color  = color

    def accelToward(self, dir):
        if(dir == Direc.UP):
            self.Accel.Y = -0.1
        if(dir == Direc.DOWN):
            self.Accel.Y = -0.1
        if(dir == Direc.LEFT):
            self.Accel.X = -0.1
        if(dir == Direc.RIGHT):
            self.Accel.X = 0.1 

    def process(self):
        self.Speed.addVector(self.Accel)

    def render(self, screen):
        pygame.draw.circle(screen, color, (self.Centre.X, self.Centre.Y), self.Radius)
