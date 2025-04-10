import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from game.cli import CLIInterface
from game.core import NumberGuessingGame

class TestCLIInterface(unittest.TestCase):
    def setUp(self):
        self.cli = CLIInterface()
        # Patch sys.exit to prevent tests from exiting
        self.exit_patcher = patch('sys.exit')
        self.mock_exit = self.exit_patcher.start()
    
    def tearDown(self):
        self.exit_patcher.stop()
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_difficulty_selection_easy(self, mock_stdout):
        """Test easy difficulty selection"""
        with patch('builtins.input', return_value='1'):
            self.cli._select_difficulty()
            self.assertEqual(self.cli.game.range_min, 1)
            self.assertEqual(self.cli.game.range_max, 50)
            self.assertEqual(self.cli.game.max_attempts, 10)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_difficulty_selection_invalid_then_valid(self, mock_stdout):
        """Test invalid then valid difficulty selection"""
        with patch('builtins.input', side_effect=['x', '2']):
            self.cli._select_difficulty()
            output = mock_stdout.getvalue()
            self.assertIn("Invalid input", output)
            self.assertEqual(self.cli.game.range_min, 1)
            self.assertEqual(self.cli.game.range_max, 100)
            self.assertEqual(self.cli.game.max_attempts, 7)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_game_flow_correct_guess(self, mock_stdout):
        """Test winning game flow"""
        # Mock the complete game sequence:
        # 1. Select medium difficulty
        # 2. Guess correctly (50)
        # 3. Don't want hint
        # 4. Don't play again
        with patch('builtins.input', side_effect=['2', '50', 'n', 'n']):
            self.cli.game = NumberGuessingGame(range_min=1, range_max=100, max_attempts=7)
            self.cli.game.secret_number = 50
            self.cli.run()
            
            output = mock_stdout.getvalue()
            self.assertIn("Correct!", output)
            self.assertIn("Attempts left: 6", output)  # Should have 6 remaining (7-1)
            self.mock_exit.assert_called_once()
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_game_flow_wrong_guesses(self, mock_stdout):
        """Test losing game flow"""
        # Mock sequence:
        # 1. Select medium difficulty
        # 2. Three wrong guesses (10, 20, 30)
        # 3. Don't play again
        with patch('builtins.input', side_effect=['2', '10', 'n', '20', 'n', '30', 'n', 'n']):
            self.cli.game = NumberGuessingGame(range_min=1, range_max=100, max_attempts=3)
            self.cli.game.secret_number = 50
            self.cli.run()
            
            output = mock_stdout.getvalue()
            self.assertIn("Too low!", output)
            self.assertIn("Game over!", output)
            self.assertIn("The number was 50", output)
            self.assertEqual(self.cli.game.attempts_left, 0)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_hint_feature(self, mock_stdout):
        """Test hint functionality"""
        # Mock sequence:
        # 1. Select medium difficulty
        # 2. Guess 30 (too low)
        # 3. Ask for hint
        # 4. Guess 70 (too high)
        # 5. Ask for hint
        # 6. Guess 50 (correct)
        # 7. Don't play again
        with patch('builtins.input', side_effect=['2', '30', 'y', '70', 'y', '50', 'n', 'n']):
            self.cli.game = NumberGuessingGame(range_min=1, range_max=100, max_attempts=10)
            self.cli.game.secret_number = 50
            self.cli.run()
            
            output = mock_stdout.getvalue()
            self.assertIn("The number is between 30 and 100", output)
            self.assertIn("The number is between 1 and 70", output)
            self.assertIn("Correct!", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_guess_handling(self, mock_stdout):
        """Test handling of invalid guesses"""
        # Mock sequence:
        # 1. Select medium difficulty
        # 2. Enter invalid guess ('x')
        # 3. Enter valid guess (50)
        # 4. Don't play again
        with patch('builtins.input', side_effect=['2', 'x', '50', 'n', 'n']):
            self.cli.game = NumberGuessingGame(range_min=1, range_max=100, max_attempts=7)
            self.cli.game.secret_number = 50
            self.cli.run()
            
            output = mock_stdout.getvalue()
            self.assertIn("Please enter a valid number", output)
            self.assertIn("Correct!", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_again_yes(self, mock_stdout):
        """Test play again functionality"""
        # Mock sequence:
        # 1. Select medium difficulty
        # 2. Guess correctly (50)
        # 3. Play again (y)
        # 4. Select easy difficulty
        # 5. Guess correctly (25)
        # 6. Don't play again
        with patch('builtins.input', side_effect=['2', '50', 'n', 'y', '1', '25', 'n', 'n']):
            self.cli.game = NumberGuessingGame(range_min=1, range_max=100, max_attempts=7)
            self.cli.game.secret_number = 50
            self.cli.run()
            
            output = mock_stdout.getvalue()
            self.assertEqual(2, output.count("Correct!"))  # Should win twice
            self.assertIn("Select difficulty", output)  # Should see difficulty selection again

if __name__ == '__main__':
    unittest.main()