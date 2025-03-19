# game.py

from board import Kulibrat
from rules import get_legal_moves

def play_human_vs_human():
    game = Kulibrat()
    while True:
        game.print_board()
        moves = get_legal_moves(game)
        if not moves:
            print("No moves! Checking next player’s turn.")
            # According to Kulibrat, if no moves, the other player goes again
            old_player = game.current_player
            game.current_player = "R" if old_player == "B" else "B"

            # Check if *that* player also has no moves => game over
            if not get_legal_moves(game):
                print(f"No moves for either player! Game ends.")
                break
            else:
                # we continue with the new current player
                continue

        # Prompt user. We might do `move = input(...)` etc.
        print("Legal moves are:")
        for i,m in enumerate(moves):
            print(f"{i}: {m}")

        choice = input("Pick a move index: ")
        try:
            idx = int(choice)
            if 0 <= idx < len(moves):
                game.make_move(moves[idx])
            else:
                print("Invalid index.")
        except ValueError:
            print("Please enter a number.")

    print("Final board state:")
    game.print_board()
    print("Game over.")
