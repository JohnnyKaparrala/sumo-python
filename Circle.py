from Position import Position2D
class Circle():
    def __init__(self,
                 pos=Position2D(0,0),
                 r=20, #radius in pixels
    ):
        self.Centre = pos
        self.Radius = Radius
    
    def distance(self, other):
        return (self.Centre.distance(other.Centre)-(self.Radius + other.Radius))

    def hasCollision(self, other):
        return self.distance(other)<=0
    