from game import Game
from vocabulary import WIDTH, HEIGHT, ground


def main():
    """
    основная функция игры, запускает всё остальное
    """
    game = Game(WIDTH, HEIGHT, ground)
    game.loop()


main()
