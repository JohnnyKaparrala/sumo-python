import math

class Vector2D():
    def __init__(self,
                 x = 0.0,
                 y = 0.0
    ):
        self.X = x
        self.Y = y

    def __add__(self, other):
        if (not isinstance(other, Vector2D)):
            raise TypeError("Subtraction not supported")

        ret = Vector2D(self.X, self.Y)

        ret.X += other.X
        ret.Y += other.Y

        return ret

    def __sub__(self, other):
        if (not isinstance(other, Vector2D)):
            raise TypeError("Subtraction not supported")

        ret = Vector2D(self.X, self.Y)

        ret.X -= other.X
        ret.Y -= other.Y

        return ret

    def __mul__(self, other):
        if (not isinstance(other, int)):
            raise TypeError("Multiplication not supported")

        ret = Vector2D(self.X, self.Y)
        ret.X = ret.X * other
        ret.Y = ret.Y * other

        return ret

    def __div__(self, other):
        if (not isinstance(other, int)):
            raise TypeError("Division not supported")

        ret = Vector2D(self.X, self.Y)
        ret.X = ret.X / other
        ret.Y = ret.Y / other

        return ret

    def __neg__(self):
        ret = Vector2D(self.X, self.Y)
        ret.X = -ret.X
        ret.Y = -ret.Y

        return ret

    def __abs__(self):
        return math.sqrt(self.X**2 + self.Y**2)

    def __str__(self):
        return "({},{})".format(self.X, self.Y)