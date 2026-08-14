"""
Connect Four CLI Game with Single-Player (AI) and Two-Player modes.
"""

import random
import time
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Player:
    name: str
    token: str
    is_ai: bool = False


class Board:
    """Manages grid state, token placement, and victory conditions."""

    ROWS: int = 6
    COLS: int = 7
    EMPTY: str = " "

    def __init__(self):
        self.grid: List[List[str]] = [
            [self.EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)
        ]

    def display(self) -> None:
        """Renders the grid with column headers and borders."""
        col_headers = "   " + "   ".join(str(i + 1) for i in range(self.COLS))
        separator = " +" + "---+" * self.COLS

        print("\n" + col_headers)
        print(separator)
        for row in self.grid:
            row_content = " | " + " | ".join(row) + " |"
            print(row_content)
            print(separator)
        print()

    def is_valid_column(self, col: int) -> bool:
        """Checks if a column index is within bounds and not full."""
        return 0 <= col < self.COLS and self.grid[0][col] == self.EMPTY

    def get_valid_columns(self) -> List[int]:
        """Returns a list of all column indices that can accept a token."""
        return [c for c in range(self.COLS) if self.is_valid_column(c)]

    def drop_token(self, col: int, token: str) -> Optional[int]:
        """Places a token in the lowest available slot of a column."""
        for r in reversed(range(self.ROWS)):
            if self.grid[r][col] == self.EMPTY:
                self.grid[r][col] = token
                return r
        return None

    def remove_token(self, row: int, col: int) -> None:
        """Clears a cell (used for AI simulation)."""
        self.grid[row][col] = self.EMPTY

    def check_win(self, token: str) -> bool:
        """Evaluates horizontal, vertical, and diagonal win conditions."""
        # 1. Horizontal check
        for r in range(self.ROWS):
            for c in range(self.COLS - 3):
                if all(self.grid[r][c + i] == token for i in range(4)):
                    return True

        # 2. Vertical check
        for r in range(self.ROWS - 3):
            for c in range(self.COLS):
                if all(self.grid[r + i][c] == token for i in range(4)):
                    return True

        # 3. Down-right diagonal (\)
        for r in range(self.ROWS - 3):
            for c in range(self.COLS - 3):
                if all(self.grid[r + i][c + i] == token for i in range(4)):
                    return True

        # 4. Up-right diagonal (/)
        for r in range(3, self.ROWS):
            for c in range(self.COLS - 3):
                if all(self.grid[r - i][c + i] == token for i in range(4)):
                    return True

        return False

    def is_full(self) -> bool:
        """Returns True if no valid moves remain."""
        return len(self.get_valid_columns()) == 0


class ConnectFourAI:
    """Heuristic rule-based AI for single-player mode."""

    @staticmethod
    def choose_column(board: Board, ai_token: str, opponent_token: str) -> int:
        valid_cols = board.get_valid_columns()
        if not valid_cols:
            return 0

        # 1. Take immediate winning move
        for col in valid_cols:
            row = board.drop_token(col, ai_token)
            if row is not None:
                if board.check_win(ai_token):
                    board.remove_token(row, col)
                    return col
                board.remove_token(row, col)

        # 2. Block immediate opponent win
        for col in valid_cols:
            row = board.drop_token(col, opponent_token)
            if row is not None:
                if board.check_win(opponent_token):
                    board.remove_token(row, col)
                    return col
                board.remove_token(row, col)

        # 3. Prioritize center and adjacent columns for board control
        center_preference = [3, 2, 4, 1, 5, 0, 6]
        for col in center_preference:
            if col in valid_cols:
                return col

        return random.choice(valid_cols)


class ConnectFourGame:
    """Manages player turns, user inputs, and round loops."""

    def __init__(self):
        self.board = Board()
        self.players: List[Player] = []
        self.current_idx = 0

    def setup_game(self) -> None:
        """Configures game mode and player identities."""
        print("=" * 40)
        print("       WELCOME TO CONNECT FOUR        ")
        print("=" * 40)
        print("1. Single Player (vs Computer)")
        print("2. Two Players (Pass & Play)")

        while True:
            choice = input("\nSelect mode (1 or 2): ").strip()
            if choice == "1":
                p1_name = input("Enter your name: ").strip() or "Player 1"
                self.players = [
                    Player(name=p1_name, token="X", is_ai=False),
                    Player(name="Computer", token="O", is_ai=True),
                ]
                break
            elif choice == "2":
                p1_name = input("Enter Player 1 name: ").strip() or "Player 1"
                p2_name = input("Enter Player 2 name: ").strip() or "Player 2"
                self.players = [
                    Player(name=p1_name, token="X", is_ai=False),
                    Player(name=p2_name, token="O", is_ai=False),
                ]
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def get_human_move(self, player: Player) -> int:
        """Prompts the user for a valid column number (1 to 7)."""
        while True:
            prompt = f"{player.name} ({player.token}), choose column (1-{self.board.COLS}): "
            user_input = input(prompt).strip()

            if not user_input.isdigit():
                print("Please enter a valid number.")
                continue

            col = int(user_input) - 1
            if not (0 <= col < self.board.COLS):
                print(f"Column must be between 1 and {self.board.COLS}.")
            elif not self.board.is_valid_column(col):
                print("That column is full. Choose another column.")
            else:
                return col

    def play_round(self) -> None:
        """Executes a full game round until a win or draw occurs."""
        self.board = Board()
        self.current_idx = 0

        while True:
            self.board.display()
            current_player = self.players[self.current_idx]
            opponent = self.players[1 - self.current_idx]

            if current_player.is_ai:
                print(f"{current_player.name} ({current_player.token}) is thinking...")
                time.sleep(0.5)
                col = ConnectFourAI.choose_column(
                    self.board, current_player.token, opponent.token
                )
                print(f"{current_player.name} played in column {col + 1}.")
            else:
                col = self.get_human_move(current_player)

            self.board.drop_token(col, current_player.token)

            # Check win condition
            if self.board.check_win(current_player.token):
                self.board.display()
                print("*" * 40)
                print(f"  🎉 {current_player.name} ({current_player.token}) WINS! 🎉")
                print("*" * 40)
                break

            # Check draw condition
            if self.board.is_full():
                self.board.display()
                print("=" * 40)
                print("  The game ended in a draw (board is full).")
                print("=" * 40)
                break

            # Switch player turn
            self.current_idx = 1 - self.current_idx

    def start(self) -> None:
        """Main game runner supporting replays."""
        self.setup_game()
        while True:
            self.play_round()
            again = input("\nWould you like to play again? [y/N]: ").strip().lower()
            if again != "y":
                print("\nThanks for playing Connect Four!")
                break


if __name__ == "__main__":
    game = ConnectFourGame()
    game.start()
