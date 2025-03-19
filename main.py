from game.board import Kulibrat
from game.rules import get_legal_moves
from agent.player import HumanPlayer
from agent.minimax_agent import MinimaxAI  # Import Minimax agent
from agent.random_agent import RandomAI


def setup_game():

    """
    First a quick welcome message with game rules
    """

    print("\nWelcome to Kulibrat! A two-player strategy game.")
    print("Rules:")
    print("- Each player has 4 pieces and takes turns inserting or moving them.")
    print("- Move pieces diagonally forward to reach the opponent's start row and score.")
    print("- You can attack an opponent's piece if directly in front.")
    print("- You can jump over an opponent’s line if the space behind is free or outside the board.")

    """
    The player will start by choosing an opponent.
    the choice can be made between: Minimax, random and human
    """

    # Choose Red Player (Opponent)
    while True:
        print("Please choose the desired opponent")
        print("0 = Human")
        print("1 = RandomAI")
        print("2 = MinimaxAI")
        choice = input("Choose Red player: ").strip()
        if choice in {"0","1","2"}:
            break
        print("Invalid choice. Enter 1 or 2.")

    if choice == "0":
        red_player_type = HumanPlayer
        print("You chose a Human opponent.")
    elif choice == "1":
        red_player_type = RandomAI
        print("You chose an AI opponent.")
    else:
        red_player_type = MinimaxAI
        print("You chose an AI opponent.")

    """
    Now the desired winning points can be chosen
    """

    # Choose Winning Points
    while True:
        try:
            winning_points = int(input("Enter winning points (1-5 recommended): ").strip())
            if winning_points > 0:
                break
        except ValueError:
            pass
        print("Invalid input. Please enter a positive number.")

    """
    Lastly, if the minimax agent is chosen,
    the player can choose the desired difficulty
    """

    # Choose AI Difficulty (Minimax Depth) - Only applies if AI is chosen
    ai_depth = 3  # Default AI depth
    if red_player_type == MinimaxAI:
        while True:
            try:
                ai_depth = int(input("Choose AI difficulty (1-5, higher is smarter): ").strip())
                if 1 <= ai_depth <= 5:
                    break
            except ValueError:
                pass
            print("Invalid input. Enter a number between 1 and 5.")

    return red_player_type, winning_points, ai_depth

def play_game():

    red_player_type, winning_points, ai_depth = setup_game()

    game = Kulibrat()
    black_player = HumanPlayer(game)

    if red_player_type == MinimaxAI:
        red_player = red_player_type(game, ai_depth)  # Set AI depth (increase for smarter AI)
    else:
        red_player = red_player_type(game)

    if winning_points == 1:
        print("- The first player to reach", winning_points, "point wins!")
    else:
        print("- The first player to reach", winning_points, "points wins!")

    print("")

    # Print board normally with B and R for players
    # Print column headers
    print("     " + "   ".join(str(i) for i in range(3)))
    print("    --" + "---" * 3)

    # Print each row with lettered row index
    for i, row in enumerate(game.board):
        print(f" {chr(65 + i)} | " + " | ".join(row) + " |")
        print("    --" + "---" * 3)

    print("")

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
