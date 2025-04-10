import argparse
from game.cli import CLIInterface
from game.gui import GUIInterface

def main():
    parser = argparse.ArgumentParser(description="Number Guessing Game")
    parser.add_argument('--gui', action='store_true', help='Launch graphical version')
    args = parser.parse_args()
    
    if args.gui:
        game = GUIInterface()
    else:
        game = CLIInterface()
    
    game.run()

if __name__ == "__main__":
    main()