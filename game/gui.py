import PySimpleGUI as sg
from .core import NumberGuessingGame

class GUIInterface:
    """Graphical user interface for the number guessing game."""
    
    def __init__(self):
        self.game = NumberGuessingGame()
        self.theme = 'DarkBlue3'
        sg.theme(self.theme)
        
    def create_main_window(self):
        """Create and return the main game window."""
        layout = [
            [sg.Text("Number Guessing Game", font=('Helvetica', 20))],
            [sg.Text("I'm thinking of a number between 1 and 100", key='-RANGE-')],
            [sg.Text("Attempts left: 7", key='-ATTEMPTS-')],
            [sg.Input(size=(10, 1), key='-GUESS-'), sg.Button('Guess')],
            [sg.Text("", size=(30, 2), key='-FEEDBACK-')],
            [sg.Button('New Game'), sg.Button('Hint'), sg.Button('Exit')],
            [sg.Text("", size=(30, 1), key='-SCORE-')]
        ]
        return sg.Window("Number Guessing Game", layout)
    
    def run(self):
        """Main game loop for GUI."""
        window = self.create_main_window()
        self.game.start_new_game()
        
        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
                
            elif event == 'New Game':
                self.game.start_new_game()
                window['-FEEDBACK-'].update("")
                window['-ATTEMPTS-'].update(f"Attempts left: {self.game.attempts_left}")
                window['-SCORE-'].update("")
                window['-GUESS-'].update("")
                
            elif event == 'Guess':
                try:
                    guess = int(values['-GUESS-'])
                    feedback, game_over = self.game.make_guess(guess)
                    window['-FEEDBACK-'].update(feedback)
                    window['-ATTEMPTS-'].update(f"Attempts left: {self.game.attempts_left}")
                    window['-GUESS-'].update("")
                    
                    if game_over and self.game.won:
                        window['-SCORE-'].update(f"Your score: {self.game._calculate_score()}")
                except ValueError:
                    window['-FEEDBACK-'].update("Please enter a valid number!")
                    
            elif event == 'Hint':
                hint = self.game.get_hint()
                if hint:
                    window['-FEEDBACK-'].update(f"Hint: {hint}")
                else:
                    window['-FEEDBACK-'].update("No hint available")
        
        window.close()