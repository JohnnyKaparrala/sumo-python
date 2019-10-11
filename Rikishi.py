from Directions import Directions as Direc
from Acceleration import Acceleration2D, Speed2D
from Circle import Circle
from Position import Position2D
import pygame

class Rikishi(Circle):
    
    def __init__(self,
                 pos=Position2D(0,0),
                 r=20, #radius in pixels
                 color = (155, 0, 0)
    ):
        self.Centre = pos                 #(pixel, pixel)
        self.Radius = r                   #pixel
        self.Speed  = Speed2D(0,0)        #pixel/update
        self.Accel  = Acceleration2D(0,0) #pixel/update**2
        self.Color  = color

    def accelToward(self, dir):
        if(dir == Direc.UP):
            self.Accel.Y = -0.1
        if(dir == Direc.DOWN):
            self.Accel.Y = 0.1
        if(dir == Direc.LEFT):
            self.Accel.X = -0.1
        if(dir == Direc.RIGHT):
            self.Accel.X = 0.1

    def stopAccelToward(self, dir):
        if(dir == Direc.UP):
            self.Accel.Y = 0
        if(dir == Direc.DOWN):
            self.Accel.Y = 0
        if(dir == Direc.LEFT):
            self.Accel.X = 0
        if(dir == Direc.RIGHT):
            self.Accel.X = 0

    def transferMomentum(self, other):
        #errado
        self.Speed.subtractVector(other.Speed)

    def stopMov(self):
        self.Speed  = Speed2D(0,0)        
        self.Accel  = Acceleration2D(0,0)

    def process(self):
        self.Speed.addVector(self.Accel)       
        self.Centre.X += self.Speed.X
        self.Centre.Y += self.Speed.Y

    def render(self, screen):
        pygame.draw.circle(screen, self.Color, self.Centre.toTuple(), self.Radius)

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
                                int(string[string.find('Rikishi at (')+12:string.find(',')]),
                                int(string[string.find(',')+1: string.find(')')])
                                )
        self.Radius = int(string[string.find('Radius = ')+9: string.find(';', string.find('Radius = '))])
        self.Speed = Speed2D(
                                int(string[string.find('Speed = (')+9:string.find(',', string.find('Speed = ('))]),
                                int(string[string.find(',',string.find('Speed = ('))+1:string.find(')',string.find('Speed = ('))])
                            )
        self.Accel = Speed2D(
                                int(string[string.find('Acceleration = (')+16:string.find(',', string.find('Acceleration = ('))]),
                                int(string[string.find(',',string.find('Acceleration = ('))+1:string.find(')',string.find('Acceleration = ('))])
                            )
        self.Color = (
                        int(string[string.find('Color = (')+9:string.find(',', string.find('Color = ('))]),
                        int(string[string.find(',', string.find('Color = ('))+1: string.find(',', string.find(',', string.find('Color = ('))+1)]),
                        int(string[string.find(',', string.find(',', string.find('Color = ('))+1)+1: string.find(')', string.find(',', string.find('Color = ('))+1)])
                     )


#testing Rikishi constructor and toString
"""x = Rikishi(r = 5, pos = Position2D(5,5), color=(5,5,5))
print(x)"""

#tests fromStr def
"""y = Rikishi()
print(y)
y.fromStr(x.__str__())
print(y)"""

#
