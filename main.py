from game import Game
from vocabulary import WIDTH, HEIGHT, ground
from generate_OOO import generate_ooo


def main():
    """
    основная функция игры, запускает всё остальное
    """
    generate_ooo()
    game = Game(WIDTH, HEIGHT, ground)
    game.loop()


main()
