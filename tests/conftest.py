import pytest
from game.core import NumberGuessingGame

@pytest.fixture
def game_instance():
    """Fixture providing a pre-configured game instance"""
    game = NumberGuessingGame(range_min=1, range_max=10, max_attempts=3)
    game.secret_number = 5  # Set known value
    return game