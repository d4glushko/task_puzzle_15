import pytest
from app.environment import PuzzleEnvironment, PuzzleEnvironmentSettings, PuzzleEnvironmentNotReadyException, PuzzleEnvironmentException, PuzzleAction


test_rows_and_cols = [
    (2, 2), 
    (5, 5),
    (500, 500)
]


@pytest.mark.parametrize("rows, cols", [
    (1, 1),
    (-1, -1)
])
def test_incorrect_settings(rows, cols):
    # Arrange, Act, Assert
    with pytest.raises(PuzzleEnvironmentException):
        PuzzleEnvironmentSettings(rows, cols)


@pytest.mark.parametrize("rows, cols", test_rows_and_cols)
def test_get_state(rows, cols):
    # Arrange
    env = PuzzleEnvironment(PuzzleEnvironmentSettings(rows, cols))
    env.setup()

    # Act
    state = env.get_state()

    # Assert
    for i in range(rows):
        for j in range(cols):
            assert state[i][j] is None or (state[i][j] >= 1 and state[i][j] < rows*cols)


@pytest.mark.parametrize("rows, cols", test_rows_and_cols)
def test_get_state_with_exception(rows, cols):
    # Arrange
    env = PuzzleEnvironment(PuzzleEnvironmentSettings(rows, cols))

    # Act, Assert
    with pytest.raises(PuzzleEnvironmentNotReadyException):
        env.get_state()


@pytest.mark.parametrize("rows, cols", test_rows_and_cols)
def test_environment_setup_unique_values(rows, cols):
    # Arrange
    env = PuzzleEnvironment(PuzzleEnvironmentSettings(rows, cols))

    # Act
    env.setup()

    # Assert
    assert_unique_values(env.get_state(), rows, cols)


test_rows_and_cols_and_actions = []
actions = [1, 2, 3, 4]
for el in test_rows_and_cols:
    test_rows_and_cols_and_actions.extend([(el[0], el[1], PuzzleAction(action)) for action in actions])
@pytest.mark.parametrize("rows, cols, action", test_rows_and_cols_and_actions)
def test_act(rows, cols, action):
    # Arrange
    env = PuzzleEnvironment(PuzzleEnvironmentSettings(rows, cols))
    env.setup()
    old_none_position = get_none_position(env.get_state(), rows, cols)

    # Act
    env.act(action)

    # Assert
    new_state = env.get_state()
    new_none_position = get_none_position(new_state, rows, cols)
    assert_unique_values(new_state, rows, cols)

    if action == PuzzleAction.UP and old_none_position[0] == rows - 1 or \
        action == PuzzleAction.DOWN and old_none_position[0] == 0 or \
        action == PuzzleAction.LEFT and old_none_position[1] == cols - 1 or \
        action == PuzzleAction.RIGHT and old_none_position[1] == 0:
        assert old_none_position == new_none_position
    else:
        if action == PuzzleAction.UP:
            assert old_none_position[0] + 1 == new_none_position[0]
            assert old_none_position[1] == new_none_position[1]
        elif action == PuzzleAction.DOWN:
            assert old_none_position[0] - 1 == new_none_position[0]
            assert old_none_position[1] == new_none_position[1]
        elif action == PuzzleAction.LEFT:
            assert old_none_position[0] == new_none_position[0]
            assert old_none_position[1] + 1 == new_none_position[1]
        elif action == PuzzleAction.RIGHT:
            assert old_none_position[0] == new_none_position[0]
            assert old_none_position[1] - 1 == new_none_position[1]


@pytest.mark.parametrize("rows, cols, action", test_rows_and_cols_and_actions)
def test_act_with_not_ready_exception(rows, cols, action):
    # Arrange
    env = PuzzleEnvironment(PuzzleEnvironmentSettings(rows, cols))

    # Act, Assert
    with pytest.raises(PuzzleEnvironmentNotReadyException):
        env.act(action)


test_rows_and_cols_and_incorrect_actions = []
incorrect_actions = [-1, 0, "a", 7, None]
for el in test_rows_and_cols:
    test_rows_and_cols_and_incorrect_actions.extend([(el[0], el[1], action) for action in incorrect_actions])
@pytest.mark.parametrize("rows, cols, action", test_rows_and_cols_and_incorrect_actions)
def test_act_with_incorrect_action_exception(rows, cols, action):
    # Arrange
    env = PuzzleEnvironment(PuzzleEnvironmentSettings(rows, cols))

    # Act, Assert
    with pytest.raises(PuzzleEnvironmentException):
        env.act(action)


@pytest.mark.parametrize("rows, cols", test_rows_and_cols)
def test_is_completed(rows, cols):
    # Arrange
    env = PuzzleEnvironment(PuzzleEnvironmentSettings(rows, cols))
    env.setup()

    # Act
    # import pdb; pdb.set_trace()
    env._PuzzleEnvironment__env = generate_completed_env(rows, cols)
    env._PuzzleEnvironment__empty_position = (rows - 1, cols - 1)
    is_completed = env.is_completed()

    # Assert
    assert is_completed


@pytest.mark.parametrize("rows, cols", test_rows_and_cols)
def test_is_not_completed_middle_elements(rows, cols):
    # Arrange
    env = PuzzleEnvironment(PuzzleEnvironmentSettings(rows, cols))
    env.setup()

    # Act
    env._PuzzleEnvironment__env = generate_completed_env(rows, cols)
    env._PuzzleEnvironment__empty_position = (rows - 1, cols - 1)
    buf = env._PuzzleEnvironment__env[0][0]
    env._PuzzleEnvironment__env[0][0] = env._PuzzleEnvironment__env[0][1]
    env._PuzzleEnvironment__env[0][1] = buf
    is_completed = env.is_completed()

    # Assert
    assert not is_completed


@pytest.mark.parametrize("rows, cols", test_rows_and_cols)
def test_is_not_completed_none_element(rows, cols):
    # Arrange
    env = PuzzleEnvironment(PuzzleEnvironmentSettings(rows, cols))
    env.setup()

    # Act
    env._PuzzleEnvironment__env = generate_completed_env(rows, cols)
    env._PuzzleEnvironment__empty_position = (rows - 1, cols - 1)
    env.act(PuzzleAction.DOWN)
    is_completed = env.is_completed()

    # Assert
    assert not is_completed


@pytest.mark.parametrize("rows, cols", test_rows_and_cols)
def test_is_completed_with_exception(rows, cols):
    # Arrange
    env = PuzzleEnvironment(PuzzleEnvironmentSettings(rows, cols))

    # Act, Assert
    with pytest.raises(PuzzleEnvironmentNotReadyException):
        env.is_completed()


def generate_completed_env(rows, cols):
    result = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if i == rows - 1 and j == cols - 1:
                value = None
            else:
                value = i * cols + j + 1
            row.append(value)
        result.append(row)
    return result


def assert_unique_values(state, rows, cols):
    value_counts = [0 for _ in range(rows * cols)]
    for i in range(rows):
        for j in range(cols):
            value = state[i][j] if state[i][j] is not None else rows * cols
            assert value_counts[value - 1] == 0
            value_counts[value - 1] += 1


def get_none_position(state, rows, cols):
    none_position = None
    i, j = 0, 0
    while (none_position is None and i < rows and j < cols):
        if state[i][j] is None:
                none_position = (i, j)
        j += 1
        if j >= cols:
            i += 1
            j = 0
    assert none_position is not None
    return none_position
