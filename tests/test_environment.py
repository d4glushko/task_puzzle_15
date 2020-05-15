import pytest
from app.environment import PuzzleEnvironment, PuzzleEnvironmentSettings

def test_environment_setup():
    env = PuzzleEnvironment(PuzzleEnvironmentSettings(4, 4))
    env.setup()
    assert len(env.get_state()) > 0
