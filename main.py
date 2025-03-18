from game.board import Kulibrat
from game.rules import get_legal_moves
from agent.player import HumanPlayer
from agent.minimax_agent import MinimaxAI  # Import Minimax agent

def play_game():
    game = Kulibrat()
    black_player = HumanPlayer(game)
    red_player = MinimaxAI(game, depth=3)  # Set AI depth (increase for smarter AI)

    winning_points = 5  # Decide the winning threshold

    while True:
        # -------------------
        # BLACK TURN
        # -------------------
        black_moves = get_legal_moves(game)
        if black_moves:
            chosen = black_player.choose_move(black_moves)
            if chosen is not None:
                game.make_move(chosen)
                if game.scores["B"] >= winning_points:
                    print("Black reaches enough points! Game Over.")
                    break
            else:
                print("No move returned for Black—skipping.")
        else:
            print("Black has no moves.")

        # -------------------
        # RED TURN (AI - Minimax)
        # -------------------
        red_moves = get_legal_moves(game)
        if red_moves:
            chosen = red_player.choose_move(red_moves)
            if chosen is not None:
                print(f"🤖 AI chooses: {chosen}")  # Let player see AI's move
                game.make_move(chosen)
                if game.scores["R"] >= winning_points:
                    print("Red reaches enough points! Game Over.")
                    break
            else:
                print("No move returned for Red—skipping.")
        else:
            print("Red has no moves.")

        # -------------------
        # PRINT BOARD ONCE PER ROUND
        # -------------------
        game.print_board()

        # If both players have no moves left, end the game
        if not black_moves and not red_moves:
            print("Neither player can move => game ends.")
            break

    # Final board state
    print("Final board state:")
    game.print_board()
    print(f"Final Score: 👤={game.scores['B']}  🤖={game.scores['R']}")

if __name__ == "__main__":
    play_game()
