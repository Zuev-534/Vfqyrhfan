from vocabulary import *


def generate_emp(a, b, c):
    return np.zeros((a, b, c), dtype='B')


class Scene:
    def __init__(self):
        self.map = generate_emp(1000, 1000, 1000)

    def test(self):
        for i in range(20):
            for k in range(20):
                self.map[510 + i][521 + k][10] = 4

        self.map[10][21][13] = 4


if __name__ == "__main__":
    print("This module is not for direct call!")
