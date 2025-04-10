import random
from typing import Tuple, Optional

class NumberGuessingGame:
    """Core logic for the number guessing game."""
    
    DEFAULT_RANGE = (1, 100)
    DEFAULT_ATTEMPTS = 7
    
    def __init__(self, range_min: int = None, range_max: int = None, max_attempts: int = None):
        """Initialize game with optional custom range and attempts."""
        self.range_min = range_min or self.DEFAULT_RANGE[0]
        self.range_max = range_max or self.DEFAULT_RANGE[1]
        self.max_attempts = max_attempts or self.DEFAULT_ATTEMPTS
        self.secret_number = None
        self.attempts_left = 0
        self.guesses = []
        self.game_over = False
        self.won = False
        
    def start_new_game(self) -> None:
        """Reset game state and generate new secret number."""
        self.secret_number = random.randint(self.range_min, self.range_max)
        self.attempts_left = self.max_attempts
        self.guesses = []
        self.game_over = False
        self.won = False
    
    def make_guess(self, guess: int) -> Tuple[str, bool]:
        """
        Process a player's guess.
        Returns (feedback_message, is_game_over)
        """
        if self.game_over:
            return "Game is already over!", True
            
        if guess < self.range_min or guess > self.range_max:
            return f"Guess must be between {self.range_min} and {self.range_max}", False
            
        self.attempts_left -= 1
        self.guesses.append(guess)
        
        if guess == self.secret_number:
            self.game_over = True
            self.won = True
            score = self._calculate_score()
            return f"Correct! Your score: {score}", True
        elif self.attempts_left == 0:
            self.game_over = True
            return f"Game over! The number was {self.secret_number}", True
        elif guess < self.secret_number:
            return "Too low!", False
        else:
            return "Too high!", False
    
    def _calculate_score(self) -> int:
        """Calculate score based on attempts and range size."""
        if not self.won:
            return 0
        range_size = self.range_max - self.range_min
        attempt_weight = (self.attempts_left / self.max_attempts) * 100
        base_score = (100 / range_size) * 100  # Normalize for range
        return int(base_score * (attempt_weight / 100))
    
    def get_hint(self) -> Optional[str]:
        """Provide a hint without ending the game."""
        if self.game_over or not self.guesses:
            return None
            
        last_guess = self.guesses[-1]
        if last_guess < self.secret_number:
            return f"The number is between {last_guess} and {self.range_max}"
        else:
            return f"The number is between {self.range_min} and {last_guess}"