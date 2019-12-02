from Position import Position2D
class Circle():
    def __init__(self,
                 pos=Position2D(0,0),
                 r=20.0, #radius in pixels
    ):
        self.Centre = pos
        self.Radius = r
    
    def distance(self, other):
        if isinstance(other, Circle):
            return (self.Centre.distance(other.Centre)-(self.Radius + other.Radius))
        else:
            raise TypeError("Colission not supported for this type")

    def hasCollision(self, other):
        if isinstance(other, Circle):
            return self.distance(other)<=0
        else:
            raise TypeError("Colission not supported for this type")
    