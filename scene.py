from vocabulary import *


def generate_emp(a, b, c):
    return np.zeros((a, b, c), dtype='B')


class Scene:
    def __init__(self):
        self.map = generate_emp(1000, 1000, 1000)

    def test(self):
        self.map[10][21][10] = 4



if __name__ == "__main__":
    print("This module is not for direct call!")
