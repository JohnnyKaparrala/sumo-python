import math

class Position2D():
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def distance(self, pos2):
        return math.sqrt((self.X - pos2.X)**2 + (self.Y - pos2.Y)**2)

    def toTuple(self):
        return (int(self.X), int(self.Y))
    
    def __str__(self):
        return "({}, {})".format(self.X, self.Y)

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y 
