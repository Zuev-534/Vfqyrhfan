from vocabulary import *


def generate_emp(a, b, c):
    """
    создаёт начальную карту, в которой в последующем будут храниться блоки
    """
    return np.zeros((a, b, c), dtype='B')


class Scene:
    def __init__(self):
        self.map = generate_emp(1000, 1000, 1000)

    def test(self):
        """
        функция, создаёт начальный пул блоков на карте
        return: None
        """
        for i in range(20):
            for k in range(20):
                self.map[51 + i][52 + k][10] = 4

    def dest_block(self, fat):
        """
        уничтожает выделенный блок
        fat: выделенный блок
        return: None
        """
        if not isinstance(fat, type(None)):
            self.map[fat[0]][fat[1]][fat[2]] = 0

    def add_block(self, fat, color):
        """
        добавляет блок на карту
        fat:координата выделенного блока
        color: цвет, которым станет блок
        return: None
        """
        if not isinstance(fat, type(None)):
            self.map[fat[0] + fat[4][0]][fat[1] + fat[4][1]][fat[2] + fat[4][2]] = color


if __name__ == "__main__":
    print("This module is not for direct call!")
