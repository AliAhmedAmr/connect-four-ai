# Connect Four CLI with Heuristic AI

A modular, zero-dependency command-line implementation of Connect Four in Python supporting both Single-Player (vs. Computer AI) and Two-Player Pass & Play modes.

## Features
- **Smart AI Opponent**: Uses a lookahead decision algorithm that seeks immediate wins, blocks opponent threats, and prioritizes board center control.
- **Two Game Modes**: Single-player vs. AI or local 2-player pass-and-play.
- **Clean Architecture**: Separation of concerns across `Board` state management, `ConnectFourAI` heuristics, and `ConnectFourGame` orchestration.
- **Robust Input Handling**: Bounds checking, full-column detection, and replay support.

## How to Play

### Prerequisites
- Python 3.9 or newer

### Instructions
1. Clone or download the repository.
2. Run the game from your terminal:
   ```bash
   python main.py
