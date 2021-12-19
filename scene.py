from vocabulary import *


def generate_emp(a, b, c):
    return np.zeros((a, b, c), dtype='B')


class Scene:
    def __init__(self):
        """
        генерирует массив, в которые можно записывать кубы
        """
        self.map = generate_emp(100, 100, 50)

    def test(self):
        for i in range(10):
            for k in range(10):
                self.map[51 + i][52 + k][10] = 4



if __name__ == "__main__":
    print("This module is not for direct call!")
