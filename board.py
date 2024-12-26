import numpy as np

PLAYER1 = 1
PLAYER2 = 2
RESULT_DRAW = 99


class Board:
    ROWS = 6
    COLUMNS = 7

    def __init__(self):
        self.grid = [[0] * COLS for _ in range(ROWS)]
        self.current_player = PLAYER1
        self.column = 0

    def is_valid_move(self, column):
        """A move is valid if the top row of the column is empty."""
        return self.grid[0, column] == 0

    def make_move(self, col):
        """Makes a move in the specified column in the first available row.

        Args:
            col (int): The column to make the move in.

        Returns:
            int: The row the move was made in, or -1 if the move is invalid.
        """
        if not self.is_valid_move(col):
            return -1

        for row in range(ROWS - 1, -1, -1):
            if grid[row][col] == 0:
                grid[row][col] = self.current_player
                self.current_player = 3 - self.current_player  # Change player
                return row

    def is_gameover(self):
        """Checks if the game is over."""
        return self.get_game_result() is not None

    def get_game_result(self):
        """Checks if the game is over and returns the result.

        Returns:
            int: The result of the game, or None if the game is not over.
        """

        # Check for 4 in a row
        for row in range(self.ROWS):
            for col in range(self.COLUMNS - 3):
                if self._check_line([(row, col + i) for i in range(4)]):
                    return PLAYER1 if self.grid[row, col] == 1 else PLAYER2

        # Check for 4 in a column
        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS):
                if self._check_line([(row + i, col) for i in range(4)]):
                    return PLAYER1 if self.grid[row, col] == 1 else PLAYER2

        # Check for 4 in a diagonal
        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS - 3):
                if self._check_line([(row + i, col + i) for i in range(4)]):
                    return PLAYER1 if self.grid[row, col] == 1 else PLAYER2

        # Check for 4 in an opposite diagonal
        for row in range(self.ROWS - 3):
            for col in range(3, self.COLUMNS):
                if self._check_line([(row + i, col - i) for i in range(4)]):
                    return PLAYER1 if self.grid[row, col] == 1 else PLAYER2

        # Check for draw
        if np.all(self.grid != 0):
            return RESULT_DRAW

        return None

    def _check_line(self, positions):
        """Checks if all the positions in the list have the same value."""
        values = [self.grid[row, col] for row, col in positions]
        return values[0] != 0 and all(v == values[0] for v in values)

    def get_valid_moves(self):
        """Returns a list of valid moves."""
        return [col for col in range(self.COLUMNS) if self.is_valid_move(col)]

    def __str__(self):
        """Returns a printable string representation of the board."""
        display = {0: ".", 1: "X", 2: "O"}
        rows = [" ".join(display[val] for val in row) for row in self.grid]
        return "\n".join(rows)


def play_game(p1_strategy, p2_strategy):
    """Plays a single game between two strategies.

    Args:
        p1_strategy (function): The strategy for player 1.
        p2_strategy (function): The strategy for player 2.

    Returns:
        Board: The final board state.
    """
    board = Board()
    player_strategies = {1: p1_strategy, 2: p2_strategy}

    while not board.is_gameover():
        current_strategy = player_strategies[board.current_player]
        move = current_strategy(board)
        board.make_move(move)

    return board


def play_games(
        total_games,
        p1_strategy,
        p2_strategy,
        play_single_game=play_game):
    """Plays multiple games between two strategies and prints the results.

    Args:
        total_games (int): The number of games to play.
        p1_strategy (function): The strategy for player 1.
        p2_strategy (function): The strategy for player 2.
        play_single_game (function, optional): The function to play a single game. Defaults to play_game.

    Returns:
        dict: A dictionary containing the results of the games
    """
    results = {
        PLAYER1: 0,
        PLAYER2: 0,
        RESULT_DRAW: 0
    }

    for _ in range(total_games):
        final_board = play_single_game(p1_strategy, p2_strategy)
        result = final_board.get_game_result()
        results[result] += 1

    print(f"X wins: {results[RESULT_P1_WINS] / total_games * 100:.2f}%")
    print(f"O wins: {results[RESULT_P2_WINS] / total_games * 100:.2f}%")
    print(f"Draws : {results[RESULT_DRAW] / total_games * 100:.2f}%")

    return results

# # Example strategy
# def random_strategy(board):
#     import random
#     return random.choice(board.get_valid_moves())
