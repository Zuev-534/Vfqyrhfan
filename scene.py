from vocabulary import *


def generate_emp(a, b, c):
    return np.zeros((a, b, c), dtype='B')


class Scene:
    def __init__(self):
        self.map = generate_emp(32, 32, 30)

    def test(self):
        self.map[10][21][10] = 4
        self.map[10][22][10] = 4
        self.map[10][23][10] = 4
        self.map[11][21][11] = 5
        self.map[11][22][11] = 5
        self.map[11][23][11] = 5
        self.map[11][21][10] = 3
        self.map[11][22][10] = 3
        self.map[11][23][10] = 3


if __name__ == "__main__":
    print("This module is not for direct call!")
