from game import Game
from vocabulary import ground


def main():
    """
    основная функция игры, запускает всё остальное
    """
    width, height = 1200, 720
    game = Game(width, height, ground)
    game.loop()


main()
