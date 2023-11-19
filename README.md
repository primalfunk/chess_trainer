# Python Chess Game

This is a simple chess GUI built with Python and Pygame configured to run with Stockfish and expose some of its parameters. Future versions will consider different ways of using the engine evaluation and connecting to different UCI engines.

## Description

The game allows you to play chess against a Stockfish AI opponent. The graphical chess board is rendered using Pygame.

The main components are:

- `ChessGame` - Main game class that manages game state and handles user input
- `ChessBoard` - Draws the chess board and pieces 
- `EngineDashboard` - GUI for configuring Stockfish engine settings
- `stockfish.exe` - Stockfish chess engine 

## Usage

To run the game:

                python main.py

Use the mouse to select and drag pieces to make moves. The AI opponent will automatically respond with counter moves.

The engine settings dashboard allows configuring:

- Threads
- Hash size
- Skill level
- ELO
- Limit strength
- Use NNUE

Reset button restarts the game.

## Requirements

- Python 3
- Pygame
- Python Chess
- Stockfish chess engine

## Future Improvements

Some ideas for enhancing the game:
- Add engine evaluation showing in real time
- Implement databasing for game results so the player's own game can be analyzed in depth
- Add the ability to use other chess engines


## Credits

Chess engine powered by Stockfish https://stockfishchess.org