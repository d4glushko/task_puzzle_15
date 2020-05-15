import argparse
from contextlib import contextmanager
import curses

from environment import PuzzleEnvironmentSettings
from game import PuzzleGame


@contextmanager
def terminal_window():
    window = curses.initscr()
    try:
        window.clear()
        window.keypad(True)
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        window.attron(curses.color_pair(1))
        yield window
    finally:
        curses.nocbreak()
        window.keypad(False)
        curses.echo()
        curses.flushinp()
        curses.endwin()


def main(arguments):
    with terminal_window() as window:
        puzzle_env_settings = PuzzleEnvironmentSettings(arguments.rows_number, arguments.cols_number)
        game = PuzzleGame(window, puzzle_env_settings)
        game.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows_number', type=int, default=4)
    parser.add_argument('--cols_number', type=int, default=4)

    args = parser.parse_args()
    main(args)