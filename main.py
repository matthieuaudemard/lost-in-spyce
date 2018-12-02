from game import *


if __name__ == "__main__":
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()  # creates new game
        g.run()  # run game
        g.show_go_screen()
