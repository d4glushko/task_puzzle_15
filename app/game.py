import curses

from app.environment import PuzzleEnvironment, PuzzleEnvironmentSettings, PuzzleAction
from app.views import TerminalView, AbstractView
from app.inputs import TerminalInput, AbstractInput


class CursesKeysWrapper:
    Q = 113
    ESC = 27
    R = 114
    W = 119
    KEY_UP = curses.KEY_UP
    D = 100
    KEY_RIGHT = curses.KEY_RIGHT
    S = 115
    KEY_DOWN = curses.KEY_DOWN
    A = 97
    KEY_LEFT = curses.KEY_LEFT


class PuzzleGame:
    def __init__(self, window, env_settings: PuzzleEnvironmentSettings, debug: bool):
        self.max_value = env_settings.cols_number * env_settings.rows_number - 1
        self.puzzle_env: PuzzleEnvironment = PuzzleEnvironment(env_settings)
        self.view: AbstractView = TerminalView(window, debug)
        self.input: AbstractInput = TerminalInput(window)

    def start(self):
        self.__reset_game()
        key = None

        while True:
            env_state = self.puzzle_env.get_state()
            is_completed = self.puzzle_env.is_completed()
            self.view.render_screen(self.step, env_state, key, self.max_value, is_completed)

            key = self.input.get_ch()
            if key == CursesKeysWrapper.Q or key == CursesKeysWrapper.ESC:
                break
            
            if key == CursesKeysWrapper.R:
                self.__reset_game()
                continue

            if is_completed:
                continue

            if key == CursesKeysWrapper.W or key == CursesKeysWrapper.KEY_UP:
                action = PuzzleAction.UP
            elif key == CursesKeysWrapper.D or key == CursesKeysWrapper.KEY_RIGHT:
                action = PuzzleAction.RIGHT
            elif key == CursesKeysWrapper.S or key == CursesKeysWrapper.KEY_DOWN:
                action = PuzzleAction.DOWN
            elif key == CursesKeysWrapper.A or key == CursesKeysWrapper.KEY_LEFT:
                action = PuzzleAction.LEFT
            else:
                continue
            
            self.step += 1
            self.puzzle_env.act(action)

    def __reset_game(self):
        self.puzzle_env.setup()
        self.step = 0
