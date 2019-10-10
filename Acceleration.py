class Vector():
    def __init__(self,
                 x = 0,
                 y = 0
    ):
        self.X = x
        self.Y = y

    def addVector(self, other):
        self.X += other.X
        self.Y += other.Y

    def subtractVector(self, other):
        self.X -= other.X
        self.Y -= other.Y

    def negateVector(self):
        self.X = -self.X
        self.Y = -self.Y

    def __str__(self):
        return "({},{})".format(self.X, self.Y)


class Acceleration2D(Vector):
    def __init__(self,
                 x = 0,
                 y = 0
    ):
        self.X = x
        self.Y = y

class Speed2D(Vector):
    def __init__(self,
                 x = 0,
                 y = 0
    ):
        self.X = x
        self.Y = y
