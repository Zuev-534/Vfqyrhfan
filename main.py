from game import Game
from vocabulary import ground
from generate_OOO import generate_ooo


def main():
    """
    основная функция игры, запускает всё остальное
    """
    generate_ooo()
    width, height = 1200, 720
    game = Game(width, height, ground)
    game.loop()


main()
