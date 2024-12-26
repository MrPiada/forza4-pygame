import argparse
import importlib
from prettytable import PrettyTable
from tqdm import tqdm
from board import Board
from commons import *


def play_game(p1_strategy, p2_strategy, starting_player=PLAYER1):
    """Plays a single game between two strategies.

    Args:
        p1_strategy (function): The strategy for player 1.
        p2_strategy (function): The strategy for player 2.
        starting_player (int): The player who starts the game (default is PLAYER1).

    Returns:
        Board: The final board state.
    """
    board = Board()
    board.current_player = starting_player  # Set the starting player
    player_strategies = {PLAYER1: p1_strategy, PLAYER2: p2_strategy}

    while not board.is_gameover():
        current_strategy = player_strategies[board.current_player]
        move = current_strategy.play(board)
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

    # Alternate starting player for each game
    starting_player = PLAYER1

    for _ in tqdm(range(total_games)):
        final_board = play_single_game(
            p1_strategy,
            p2_strategy,
            starting_player=starting_player
        )
        result = final_board.get_game_result()
        results[result] += 1

        # Alternate the starting player
        starting_player = PLAYER2 if starting_player == PLAYER1 else PLAYER1

    return results


def load_strategy(strategy_name):
    """
    Dynamically loads a strategy class from its module path.

    Args:
        strategy_name (str): The name of the strategy.

    Returns:
        An instance of the strategy class.

    Raises:
        ValueError: If the strategy is not found.
    """
    if strategy_name not in STRATEGY_MODULES:
        raise ValueError(f"Unknown strategy: {strategy_name}")

    module_path, class_name = STRATEGY_MODULES[strategy_name].rsplit(".", 1)
    module = importlib.import_module(module_path)
    strategy_class = getattr(module, class_name)
    return strategy_class()


def main():
    parser = argparse.ArgumentParser(
        description="Simulate games between strategies.")
    parser.add_argument(
        "--player1",
        type=str,
        choices=STRATEGY_MODULES.keys(),
        help="Strategy for Player 1.",
        default="random")
    parser.add_argument(
        "--player2",
        type=str,
        choices=STRATEGY_MODULES.keys(),
        help="Strategy for Player 2.",
        default="winnow_or_random")
    parser.add_argument("--games", type=int, default=100,
                        help="Number of games to simulate (default: 100).")

    args = parser.parse_args()

    # Load strategies
    player1_strategy = load_strategy(args.player1)
    player2_strategy = load_strategy(args.player2)

    # Simulate games
    print(
        f"Simulating {
            args.games} games between {
            args.player1} and {
                args.player2}...")
    results = play_games(args.games, player1_strategy, player2_strategy)

    # RESULTS
    table = PrettyTable()
    table.field_names = ["Outcome", "Score (%)", "Count"]
    table.add_row(
        [f"Wins: {args.player1}", f"{results[PLAYER1] / args.games * 100:.1f}%", results[PLAYER1]]
    )
    table.add_row(
        [f"Wins: {args.player2}", f"{results[PLAYER2] / args.games * 100:.1f}%", results[PLAYER2]]
    )
    table.add_row(
        ["Draws", f"{results[RESULT_DRAW] / args.games * 100:.1f}%", results[RESULT_DRAW]]
    )

    # Configura l'allineamento
    table.align["Outcome"] = "l"
    table.align["Score (%)"] = "r"
    table.align["Count"] = "r"

    print("\nResults:")
    print(table)


if __name__ == "__main__":
    main()
