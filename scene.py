from graph import Cube
from vocabulary import *

class Scene:
    def __init__(self, size=512):
        karta = []
        for i in range(32):
            slc = []
            for j in range(32):
                stolbec = []
                for k in range(30):
                    stolbec.append(Cube(i, j, k, vis=0))
                slc.append(stolbec)
            karta.append(slc)

        self.map = karta

    def test(self, sz=128):
        self.map[10][21][10].vizible = 1
        self.map[10][21][10].color = RED
        self.map[10][22][10].vizible = 1
        self.map[10][22][10].color = RED
        self.map[10][23][10].vizible = 1
        self.map[10][23][10].color = RED
        self.map[11][21][11].vizible = 1
        self.map[11][21][11].color = BLUE
        self.map[11][22][11].vizible = 1
        self.map[11][22][11].color = BLUE
        self.map[11][23][11].vizible = 1
        self.map[11][23][11].color = BLUE
        self.map[11][21][10].vizible = 1
        self.map[11][21][10].color = GREEN
        self.map[11][22][10].vizible = 1
        self.map[11][22][10].color = GREEN
        self.map[11][23][10].vizible = 1
        self.map[11][23][10].color = GREEN
