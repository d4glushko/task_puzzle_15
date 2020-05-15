import random
import enum
from typing import List, Optional, Tuple


class PuzzleEnvironmentException(Exception):
    pass


class PuzzleAction(enum.Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class PuzzleEnvironmentSettings:
    def __init__(self, rows_number: int, cols_number: int):
        self.rows_number: int = rows_number
        self.cols_number: int = cols_number


class PuzzleEnvironment:
    def __init__(self, settings: PuzzleEnvironmentSettings):
        self.__settings: PuzzleEnvironmentSettings = settings
        self.__env: Optional[List[List[Optional[int]]]] = None
        self.__empty_position: Optional[Tuple[int, int]] = None

    def setup(self):
        self.__env = []
        length = self.__settings.rows_number * self.__settings.cols_number
        values_left = [i for i in range(1, length + 1)]
        elements_count = length
        for i in range(self.__settings.rows_number):
            row = []
            for j in range(self.__settings.cols_number):
                index = random.randrange(elements_count)
                value = values_left[index]
                if value == length:
                    self.__empty_position = (i, j)
                    row.append(None)
                else:
                    row.append(value)

                values_left[index] = values_left[elements_count - 1]
                elements_count -= 1
            self.__env.append(row)

    def act(self, action: PuzzleAction):
        if not self.__is_env_ready():
            raise PuzzleEnvironmentException("Environment is not ready")

        if self.__empty_position[0] == 0 and action == PuzzleAction.DOWN or \
            self.__empty_position[1] == 0 and action == PuzzleAction.RIGHT or \
            self.__empty_position[0] == self.__settings.rows_number - 1 and action == PuzzleAction.UP or \
            self.__empty_position[1] == self.__settings.cols_number - 1 and action == PuzzleAction.LEFT:
            return

        if action == PuzzleAction.UP:
            new_pos = (self.__empty_position[0] + 1, self.__empty_position[1])
        elif action == PuzzleAction.DOWN:
            new_pos = (self.__empty_position[0] - 1, self.__empty_position[1])
        elif action == PuzzleAction.LEFT:
            new_pos = (self.__empty_position[0], self.__empty_position[1] + 1)
        elif action == PuzzleAction.RIGHT:
            new_pos = (self.__empty_position[0], self.__empty_position[1] - 1)
        else:
            raise PuzzleEnvironmentException(f"Incorrect action: {action.name}. Available actions: {[el.name for el in list(PuzzleAction)]}")

        buf = self.__env[self.__empty_position[0]][self.__empty_position[1]]
        self.__env[self.__empty_position[0]][self.__empty_position[1]] = self.__env[new_pos[0]][new_pos[1]]
        self.__env[new_pos[0]][new_pos[1]] = buf
        self.__empty_position = new_pos

    def get_state(self) -> Optional[List[List[Optional[int]]]]:
        if not self.__is_env_ready():
            raise PuzzleEnvironmentException("Environment is not ready")
        return self.__env

    def is_completed(self) -> bool:
        if not self.__is_env_ready():
            raise PuzzleEnvironmentException("Environment is not ready")

        if self.__env[self.__settings.rows_number - 1][self.__settings.cols_number - 1] is not None:
            return False

        for i in range(self.__settings.rows_number):
            for j in range(self.__settings.cols_number):
                if i == self.__settings.rows_number - 1 and j == self.__settings.cols_number - 1:
                    continue

                if self.__env[i][j] != i * self.__settings.cols_number + j + 1:
                    return False

        return True

    def __is_env_ready(self) -> bool:
        return self.__env is not None and self.__empty_position is not None
