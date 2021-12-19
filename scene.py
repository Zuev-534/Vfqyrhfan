from vocabulary import *


def generate_emp(a, b, c):
    return np.zeros((a, b, c), dtype='B')


class Scene:
    def __init__(self):
        self.map = generate_emp(1000, 1000, 1000)

    def test(self):
        for i in range(20):
            for k in range(20):
                self.map[51 + i][52 + k][10] = 4

    def dest_block(self, fat):
        if not isinstance(fat, type(None)):
            self.map[fat[0]][fat[1]][fat[2]] = 0
            print('kill')

    def add_block(self, fat, color=5):
        if not isinstance(fat, type(None)):
            self.map[fat[0] + fat[4][0]][fat[1] + fat[4][1]][fat[2] + fat[4][2]] = color
            print(fat[4])


if __name__ == "__main__":
    print("This module is not for direct call!")
