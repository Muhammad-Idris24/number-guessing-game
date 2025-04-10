import sys
from .core import NumberGuessingGame

class CLIInterface:
    """Command-line interface for the number guessing game."""
    
    def __init__(self):
        self.game = NumberGuessingGame()
        self.difficulty_settings = {
            'easy': {'range': (1, 50), 'attempts': 10},
            'medium': {'range': (1, 100), 'attempts': 7},
            'hard': {'range': (1, 200), 'attempts': 5}
        }
    
    def run(self):
        """Main game loop for CLI."""
        print("Welcome to the Number Guessing Game!")
        self._select_difficulty()
        self.game.start_new_game()
        
        while not self.game.game_over:
            print(f"\nAttempts left: {self.game.attempts_left}")
            try:
                guess = int(input("Enter your guess: "))
                feedback, game_over = self.game.make_guess(guess)
                print(feedback)
                
                if not game_over and input("Want a hint? (y/n): ").lower() == 'y':
                    hint = self.game.get_hint()
                    if hint:
                        print(f"Hint: {hint}")
            except ValueError:
                print("Please enter a valid number!")
        
        if input("\nPlay again? (y/n): ").lower() == 'y':
            self.run()
        else:
            print("Thanks for playing!")
            sys.exit()
    
    def _select_difficulty(self):
        """Let player choose difficulty level."""
        print("\nSelect difficulty:")
        for i, level in enumerate(self.difficulty_settings.keys(), 1):
            print(f"{i}. {level.capitalize()}")
        
        while True:
            try:
                choice = int(input("Enter choice (1-3): "))
                if 1 <= choice <= 3:
                    level = list(self.difficulty_settings.keys())[choice-1]
                    settings = self.difficulty_settings[level]
                    self.game = NumberGuessingGame(
                        range_min=settings['range'][0],
                        range_max=settings['range'][1],
                        max_attempts=settings['attempts']
                    )
                    break
                print("Please enter 1, 2, or 3")
            except ValueError:
                print("Invalid input. Please enter a number.")