from __future__ import annotations
import math


class Vector2:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = float(x)
        self.y = float(y)

    def set(self, v : Vector2):
        self.x = v.x
        self.y = v.y

    def clone(self):
        return Vector2(self.x, self.y)

    def __add__(self, v: Vector2):
        return Vector2(self.x + v.x, self.y + v.y)
    
    def __iadd__(self, v: Vector2):
        self.x += v.x
        self.y += v.y
        return self

    def __sub__(self, v: Vector2):
        return Vector2(self.x - v.x, self.y - v.y)
    
    def __isub__(self, v: Vector2):
        self.x -= v.x
        self.y -= v.y
        return self

    def __mul__(self, s: float):
        return Vector2(self.x * s, self.y * s)
    
    def __rmul__(self, s: float):
        return self.__mul__(s)
    
    def __truediv__(self, s: float):
        return Vector2(self.x/s, self.y/s)
    
    def __imul__(self, s: float):
        self.x *= s
        self.y *= s
        return self
    
    def length(self):
        return math.hypot(self.x, self.y)

    def dot(self, v: Vector2):
        return self.x * v.x + self.y * v.y