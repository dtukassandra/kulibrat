from game.board import Kulibrat
from game.rules import get_legal_moves
from agent.player import HumanPlayer
from agent.minimax_agent import MinimaxAI  # Import Minimax agent

def play_game():
    game = Kulibrat()
    black_player = HumanPlayer(game)
    red_player = MinimaxAI(game, depth=3)  # Set AI depth (increase for smarter AI)
    winning_points = 1  # Decide the winning threshold

    """
    Print board and pieces at the start of the game
    To initiate the game a guick list of rules will be displayed
    """
    print("\nWelcome to Kulibrat! A two-player strategy game.")
    print("Rules:")
    print("- Each player has", game.players['B'], "pieces and takes turns inserting or moving them.")
    print("- Move pieces diagonally forward to reach the opponent's start row and score.")
    print("- You can attack an opponent's piece if directly in front.")
    print("- You can jump over an opponent’s line if the space behind is free or outside the board.")

    if winning_points == 1:
        print("- The first player to reach",winning_points,"point wins!")
    else:
        print("- The first player to reach",winning_points,"points wins!")


    # Print board normally with B and R for players
    # Print column headers
    print("     " + "   ".join(str(i) for i in range(3)))
    print("    --" + "---" * 3)

    # Print each row with lettered row index
    for i, row in enumerate(game.board):
        print(f" {chr(65 + i)} | " + " | ".join(row) + " |")
        print("    --" + "---" * 3)

    # Display scores and pieces left for each player
    print(f"Pieces assigned to each player: B={game.players['B']} R={game.players['R']}")
    print("-" * 20)

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
    print(f"Final Score: B={game.scores['B']}  R={game.scores['R']}")

if __name__ == "__main__":
    play_game()
