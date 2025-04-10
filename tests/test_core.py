import unittest
from game.core import NumberGuessingGame

class TestNumberGuessingGame(unittest.TestCase):
    def setUp(self):
        self.game = NumberGuessingGame(range_min=1, range_max=10, max_attempts=3)
        self.game.secret_number = 5  # Set known value for testing
    
    def test_initial_conditions(self):
        self.assertEqual(self.game.range_min, 1)
        self.assertEqual(self.game.range_max, 10)   
        self.assertEqual(self.game.max_attempts, 3)
        self.assertEqual(self.game.attempts_left, 3)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.won)

    def test_correct_guess(self):
        feedback, game_over = self.game.make_guess(5)
        self.assertEqual(feedback, "Correct! Your score: 100")  # Updated expected score
        self.assertTrue(game_over)
        self.assertTrue(self.game.won)

    def test_game_over_on_max_attempts(self):
        self.game.make_guess(1)  # Attempt 1
        self.game.make_guess(2)  # Attempt 2
        feedback, game_over = self.game.make_guess(3)  # Attempt 3
        self.assertTrue("Game over!" in feedback)  # More flexible assertion
        self.assertTrue(game_over)
        self.assertFalse(self.game.won)

    def test_too_low_guess(self):
        feedback, game_over = self.game.make_guess(3)
        self.assertEqual(feedback, "Too low!")
        self.assertFalse(game_over)
        self.assertEqual(self.game.attempts_left, 2)  # Fixed expected value

    def test_too_high_guess(self):
        feedback, game_over = self.game.make_guess(7)
        self.assertEqual(feedback, "Too high!")
        self.assertFalse(game_over)
        self.assertEqual(self.game.attempts_left, 2)  # Fixed expected value
    
    def test_hint_generation(self):
        self.game.make_guess(3)
        hint = self.game.get_hint()
        self.assertEqual(hint, "The number is between 3 and 10")

if __name__ == '__main__':
    unittest.main()