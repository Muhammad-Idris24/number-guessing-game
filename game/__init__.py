"""
Number Guessing Game Package

Contains all modules for the number guessing game implementation.
"""

from .core import NumberGuessingGame
from .cli import CLIInterface
from .gui import GUIInterface

__all__ = ['NumberGuessingGame', 'CLIInterface', 'GUIInterface']
__version__ = '1.0.0'

# Package-level initialization if needed
print(f"Initializing number_guessing_game package version {__version__}")