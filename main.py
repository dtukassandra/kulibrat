
from game.board import Kulibrat
from game.rules import get_legal_moves
from agent.player import HumanPlayer
from agent.random_agent import RandomAI


def choose_agent(game):
    """
    Allows the user to choose an agent type for the Red player.
    """
    print("Choose agent for Red:")
    print("1. Human Player")
    print("2. Random AI")
    print("3. Minimax AI")

    while True:
        choice = input("Enter choice (1-3): ")
        if choice == "1":
            HumanPlayer()  # Use game.py for human vs human mode
            return None  # Exit after human vs human game ends
        elif choice == "2":
            return RandomAI(game)
        elif choice == "3":
            return MinimaxAI(game)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def play_game():
    """
    Runs the round-based game loop with a fixed Black player (Human) and a chosen Red player.
    """
    game = Kulibrat()

    black_player = HumanPlayer(game)  # Black player is always Human
    red_player = choose_agent(game)  # Choose an agent for Red

    if red_player is None:
        return  # Exit if human vs human mode was triggered

    players = {"Black": black_player, "Red": red_player}  # Store players as a dictionary

    winning_points = 5

    while True:
        # -------------------
        # BLACK TURN
        # -------------------
        black_moves = get_legal_moves(game, "Black", players)
        if black_moves:
            chosen = players["Black"].choose_move(black_moves)
            if chosen is not None:
                game.make_move(chosen)

        # -------------------
        # RED TURN
        # -------------------
        red_moves = get_legal_moves(game, "Red", players)
        if red_moves:
            chosen = players["Red"].choose_move(red_moves)
            if chosen is not None:
                game.make_move(chosen)

        # Print the board and check for victory
        print(game)
        if game.get_score("Black") >= winning_points:
            print("Black wins!")
            break
        if game.get_score("Red") >= winning_points:
            print("Red wins!")
            break


if __name__ == "__main__":
    play_game()



