from vocabulary import *


def generate_emp(a, b, c):
    return np.zeros((a, b, c), dtype='B')


class Scene:
    def __init__(self):
        self.map = generate_emp(1000, 1000, 1000)

    def test(self):
        self.map[10][21][10] = 4
        self.map[11][21][10] = 3
        self.map[12][21][10] = 8
        self.map[13][21][10] = 4
        self.map[10][22][10] = 5
        self.map[11][22][10] = 7
        self.map[12][22][10] = 3
        self.map[15][22][12] = 6
        self.map[16][21][11] = 5



if __name__ == "__main__":
    print("This module is not for direct call!")
