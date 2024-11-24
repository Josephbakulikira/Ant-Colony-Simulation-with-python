from functools import lru_cache

import numpy as np
from math import atan2, cos, sin, sqrt, pi
from random import uniform
import arcade

class Vector:
    def __init__(self, x=0, y=0):
        self.vec = np.array([float(x), float(y)])
        self._magnitude = None  # Cache magnitude
        self._heading = None    # Cache heading
    
    @property 
    def x(self): return self.vec[0]
    
    @property
    def y(self): return self.vec[1]
    
    @x.setter
    def x(self, value):
        self.vec[0] = float(value)
        self._reset_cache()
        
    @y.setter
    def y(self, value):
        self.vec[1] = float(value)
        self._reset_cache()
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(*(self.vec + other.vec))
        return Vector(*(self.vec + other))
        
    def __sub__(self, other):
        return Vector(*(self.vec - (other.vec if isinstance(other, Vector) else other)))
        
    def __mul__(self, other):
        return Vector(*(self.vec * (other.vec if isinstance(other, Vector) else other)))
        
    def __truediv__(self, other):
        return Vector(*(self.vec / (other.vec if isinstance(other, Vector) else other)))

    def Random(value=1):
        return Vector(uniform(-value, value), uniform(-value, value))

    def Rotate(self, angle, convertToTuple=False):
        x = self.x * cos(angle) - self.y * sin(angle)
        y = self.x * sin(angle) + self.y * cos(angle)
        if convertToTuple:
            return (x, y)
        return Vector(x, y)

    def Magnitude(self):
        if self._magnitude is None:
            self._magnitude = np.linalg.norm(self.vec)
        return self._magnitude
        
    def Normalize(self):
        mag = self.Magnitude()
        if mag > 0:
            return Vector(*(self.vec / mag))
            
    def Heading(self, toDegree=False):
        theta = atan2(self.y, self.x)
        if toDegree:
            return theta * (180/pi)
        return theta
    def SetAngle(self, angle):
        mag = self.Magnitude()
        return Vector(cos(angle) * mag, sin(angle) * mag )

    @staticmethod
    @lru_cache(maxsize=1024)
    def GetDistance(a, b):
        return np.sqrt(np.sum((a.vec - b.vec) ** 2))

    def GetDistanceSQ(a, b):
        return pow(b.x - a.x, 2) + pow(b.y - a.y, 2)

    def WithinRange(a, b, dist):
        # Quick AABB check first
        if abs(a.x - b.x) > dist or abs(a.y - b.y) > dist:
            return False
        return np.sum((a.vec - b.vec) ** 2) <= dist * dist

    def Scale(self, l):
        mag = self.Magnitude()
        if mag < 0.0001:  # Avoid division by very small numbers
            return Vector()
        return Vector(*(self.vec * (l / mag)))
        
    def Average(vecs):
        if len(vecs) == 0:
            return Vector()
        sum_vec = Vector()
        for vec in vecs:
            sum_vec += vec
        avg = sum_vec.Scale(len(vecs))  # Corrected averaging
        return avg

    def Negate(self):
        return Vector(self.x * -1, self.y * -1)
    def Copy(self):
        return Vector(self.x, self.y)
    def xy(self):
        return ( int(self.x), int(self.y) )
    def zero(self):
        return Vector(0, 0)
    def __repr__(self):
        # DEBUG
        return f" ({self.x}, {self.y})"
        
    # Reset cache when vector changes
    def _reset_cache(self):
        self._magnitude = None
        self._heading = None

# Ensure any new constants are moved to config.py
