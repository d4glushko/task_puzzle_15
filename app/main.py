import argparse
import curses
from contextlib import contextmanager

from app.environment import PuzzleEnvironmentSettings
from app.game import PuzzleGame
from app.utils import str2bool


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


def run(args):
    with terminal_window() as window:
        puzzle_env_settings = PuzzleEnvironmentSettings(args.rows_number, args.cols_number)
        game = PuzzleGame(window, puzzle_env_settings, args.debug)
        game.start()
