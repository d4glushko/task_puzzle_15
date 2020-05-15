import curses

from environment import PuzzleEnvironment, PuzzleEnvironmentSettings, PuzzleAction
from view import TerminalView


class PuzzleGame:
    def __init__(self, window, env_settings: PuzzleEnvironmentSettings):
        self.puzzle_env: PuzzleEnvironment = PuzzleEnvironment(env_settings)
        self.view: TerminalView = TerminalView(window)
        self.window = window

    def reset_game(self):
        self.puzzle_env.setup()
        self.step = 0
        env_state = self.puzzle_env.get_state()
        self.view.render_screen(self.step, env_state, None)

    def start(self):
        self.reset_game()

        while True:
            key = self.window.getch()
            if key == 113 or key == 27: # Q or Esc
                break
            
            if key == 114: # R
                self.reset_game()
                continue

            if key == 119 or key == curses.KEY_UP:
                action = PuzzleAction.UP
            elif key == 100 or key == curses.KEY_RIGHT:
                action = PuzzleAction.RIGHT
            elif key == 115 or key == curses.KEY_DOWN:
                action = PuzzleAction.DOWN
            elif key == 97 or key == curses.KEY_LEFT:
                action = PuzzleAction.LEFT
            else:
                continue
            
            self.step += 1
            self.puzzle_env.act(action)
            state = self.puzzle_env.get_state()
            self.view.render_screen(self.step, state, key)
    