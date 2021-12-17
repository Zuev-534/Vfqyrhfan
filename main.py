from game import Game
from vocabulary import WIDTH, HEIGHT


def main():
    """
    основная функция игры, запускает всё остальное
    """
    game = Game(WIDTH, HEIGHT)
    game.loop()


main()
