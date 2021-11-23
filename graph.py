from math import *
class Vector:
    def __init__(self, d0=0, dx0=0, dy0=0, dz0=0, an_xy0=0, an_xz0=0):
        self.d = d0
        self.dx = dx0
        self.dy = dy0
        self.dz = dz0
        self.an_xy = an_xy0
        self.an_xz = an_xz0
    def set_coords(self):
        self.dx = self.d*cos(self.an_xy)*cos(self.an_xz)
        self.dy = self.d*sin(self.an_xy)*cos(self.an_xz)
        self.dz = self.d*sin(self.an_xz)


