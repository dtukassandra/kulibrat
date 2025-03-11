# main.py

from game.board import Kulibrat
from game.rules import get_legal_moves
from agent.player import HumanPlayer
from agent.random_agent import RandomAI

def play_game():
    """
    This function runs our round-based game loop.
    In each round, Black moves first, then Red moves.
    We only print the board once after both players have attempted to move.
    """
    game = Kulibrat()
    black_player = HumanPlayer(game)
    red_player = RandomAI(game)

    # We'll say the first to reach 5 points wins. You can change this if you want a longer game.
    winning_points = 5

    while True:
        # -------------------
        # BLACK TURN
        # -------------------
        black_moves = get_legal_moves(game)
        if black_moves:
            # If Black has valid moves, let the human pick one
            chosen = black_player.choose_move(black_moves)
            if chosen is not None:
                # Apply the chosen move
                game.make_move(chosen)
                # Check if Black reached our winning threshold
                if game.scores["B"] >= winning_points:
                    print("Black reaches enough points! Game Over.")
                    break
            else:
                print("No move returned for Black—skipping.")
        else:
            print("Black has no moves.")

        # We'll check if the game is over only after Red tries to move too

        # -------------------
        # RED TURN
        # -------------------
        red_moves = get_legal_moves(game)
        if red_moves:
            # If Red has valid moves, let the random agent pick one
            chosen = red_player.choose_move(red_moves)
            if chosen is not None:
                game.make_move(chosen)
                # Check if Red reached the winning threshold
                if game.scores["R"] >= winning_points:
                    print("Red reaches enough points! Game Over.")
                    break
            else:
                print("No move returned for Red—skipping.")
        else:
            print("Red has no moves.")

        # -------------------
        # ONE PRINT PER ROUND
        # -------------------
        # We only call print_board() here, so we see
        # the state after both Black and Red have moved.
        game.print_board()

        # If both players had no moves, let's end the game immediately
        if not black_moves and not red_moves:
            print("Neither player can move => game ends.")
            break

    # After the loop finishes, let's show the final state
    print("Final board state:")
    game.print_board()
    print(f"Final Score: B={game.scores['B']}  R={game.scores['R']}")

if __name__ == "__main__":
    play_game()
