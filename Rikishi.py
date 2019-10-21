from Directions import Directions as Direc
from Vector import Vector2D
from Circle import Circle
from Position import Position2D
import pygame
import os

class Rikishi(Circle):
    
    def __init__(self,
                 pos=Position2D(0,0),
                 r=20.0, #radius in pixels
                 color = (155, 0, 0),
                 image_path = "rikishi_verde.png"
    ):
        self.Centre = pos           #(pixel, pixel)
        self.Radius = r             #pixel
        self.Speed  = Vector2D(0,0) #pixel/update
        self.Accel  = Vector2D(0,0) #pixel/update**2
        self.Color  = color
        self.Image = pygame.image.load(os.path.join(image_path))

    def convert_image ():
        self.Image.convert()

    def accelToward(self, dir):
        if(not isinstance(dir, Direc)):
            raise TypeError("The direction has to be a Directions obj")

        if(dir == Direc.UP):
            self.Accel.Y = -0.1
        if(dir == Direc.DOWN):
            self.Accel.Y = 0.1
        if(dir == Direc.LEFT):
            self.Accel.X = -0.1
        if(dir == Direc.RIGHT):
            self.Accel.X = 0.1

    def stopAccelToward(self, dir):
        if(not isinstance(dir, Direc)):
            raise TypeError("The direction has to be a Directions obj")

        if(dir == Direc.UP):
            self.Accel.Y = 0
        if(dir == Direc.DOWN):
            self.Accel.Y = 0
        if(dir == Direc.LEFT):
            self.Accel.X = 0
        if(dir == Direc.RIGHT):
            self.Accel.X = 0

    def transferMomentum(self, other):
        #errado: sujeito a modificações
        if (not isinstance(other, Rikishi)):
            raise TypeError("Needs to be Rikishi obj")
        
        other.Speed += self.Speed*1
        self.Speed = -self.Speed*1

    def stopMov(self):
        self.Speed  = Vector2D(0,0)
        self.Accel  = Vector2D(0,0)

    def process(self):
        self.Speed = self.Speed + self.Accel   
        self.Centre.X += self.Speed.X
        self.Centre.Y += self.Speed.Y

    def render(self, screen):
        screen.blit(self.Image, (self.Centre.X - 23, self.Centre.Y - 20))

    def __str__(self):
        return "Rikishi at {};Radius = {}; Speed = {}; Acceleration = {}; Color = {}".format(
            self.Centre.__str__(),
            self.Radius.__str__(),
            self.Speed.__str__(),
            self.Accel.__str__(),
            self.Color.__str__()
        )

    def fromStr(self, string):
        self.Centre = Position2D(
                                float(string[string.find('Rikishi at (')+12:string.find(',')]),
                                float(string[string.find(',')+1: string.find(')')])
                                )
        self.Radius = float(string[string.find('Radius = ')+9: string.find(';', string.find('Radius = '))])
        self.Speed = Vector2D(
                                float(string[string.find('Speed = (')+9:string.find(',', string.find('Speed = ('))]),
                                float(string[string.find(',',string.find('Speed = ('))+1:string.find(')',string.find('Speed = ('))])
                            )
        self.Accel = Vector2D(
                                float(string[string.find('Acceleration = (')+16:string.find(',', string.find('Acceleration = ('))]),
                                float(string[string.find(',',string.find('Acceleration = ('))+1:string.find(')',string.find('Acceleration = ('))])
                            )
        self.Color = (
                        int(string[string.find('Color = (')+9:string.find(',', string.find('Color = ('))]),
                        int(string[string.find(',', string.find('Color = ('))+1: string.find(',', string.find(',', string.find('Color = ('))+1)]),
                        int(string[string.find(',', string.find(',', string.find('Color = ('))+1)+1: string.find(')', string.find(',', string.find('Color = ('))+1)])
                     )


#testing Rikishi constructor and toString
"""x = Rikishi(r = 5, pos = Position2D(5.9,5.9), color=(5,5,5))
print(x)"""

#tests fromStr def
"""y = Rikishi()
print(y)
y.fromStr(x.__str__())
print(y)"""

#
