from game.board import Kulibrat
from game.rules import get_legal_moves
from agent.player import HumanPlayer
from agent.minimax_agent import MinimaxAI  # Import Minimax agent
from agent.random_agent import RandomAI
import os
import csv

def setup_game():

    """
    First a quick welcome message with game rules
    """

    print("\nWelcome to Kulibrat! A two-player strategy game.")
    print("")
    print("Rules:")
    print("- Each player has 4 pieces and takes turns inserting or moving them.")
    print("- Move pieces diagonally forward to reach the opponent's start row and score.")
    print("- You can attack an opponent's piece if directly in front.")
    print("- You can jump over an opponent’s line if the space behind is free or outside the board.")

    """
    The player will start by choosing an opponent.
    the choice can be made between: Minimax, random and human
    """
    ai_depth_red = 3
    ai_depth_black = 3

    while True:
        print("Choose whether you are playing or benchmarking")
        print("0 - Playing")
        print("1 - Benchmarking")
        print("")
        choice = input("Your choice: ")
        if choice == "1":
            print("Choose the AI for the black player:")
            print("0 - MinimaxAI")
            print("1 - RandomAI")
            choice = input("Your choice: ")

            if choice == "0":
                black_player_type = MinimaxAI
                try:
                    ai_depth_black = int(input(
                        "Please choose the desired difficulty for the AI between 1 and 5 (higher is smarter): ").strip())
                    if 1 <= ai_depth_black <= 5:
                        break
                except ValueError:
                    pass
                print("Invalid input. Invalid input. Enter a number between 1 and 5.")
                break

            elif choice == "1":
                black_player_type = RandomAI
                break

            else:
                pass
                print("Invalid input. Please write the name of the AI.")

        elif choice == "0":
            black_player_type = HumanPlayer
            print("You are playing")
            break

        else:
            pass
            print("Invalid input. Please write the number 0 or 1.")


    while True:
        print("Please choose the AI for the red player:")
        print("0 - Human")
        print("1 - RandomAI")
        print("2 - MinimaxAI")
        print("")
        choice = input("Opponent:").strip()
        if choice not in {"0","1","2"}:
            pass
            print("")
            print("Invalid choice. Enter 0, 1 or 2.")

        else:

            if choice == "0":
                red_player_type = HumanPlayer
                print("You chose a Human opponent!")
                print("This is a two-player game, and you will each take turns to move.")
                break
            elif choice == "1":
                red_player_type = RandomAI
                print("You chose the RandomAI opponent!")
                print("This AI will only pick a random move from the list of valid moves.")
                break
            else:
                red_player_type = MinimaxAI
                print("You chose the MinimaxAI opponent!")
                print("This AI will choose the best option based on the minimax algorithm")

                """
                the player should now choose the desired difficulty
                """

                while True:
                    print("")
                    try:
                        ai_depth_red = int(input("Please choose the desired difficulty for the AI between 1 and 5 (higher is smarter): ").strip())
                        if 1 <= ai_depth_red <= 5:
                            break
                    except ValueError:
                        pass
                    print("Invalid input. Enter a number between 1 and 5.")
                break


    """
    Lastly, the desired winning points can be chosen
    """

    while True:
        print("")
        try:
            winning_points = int(input("Enter winning points (1-5 recommended): ").strip())
            if winning_points > 0:
                break
        except ValueError:
            pass
        print("Invalid input. Please enter a positive number.")


    return red_player_type, black_player_type, winning_points, ai_depth_black, ai_depth_red


def benchmark_game():
    print("Benchmarking...")

    """
    Running the benchmark
    """
    benchmark_size = 10
    results = []  # Store results as a list of tuples (Game, Winner, Turns)

    for game_num in range(1, benchmark_size + 1):
        print(f"Starting Benchmark Game {game_num}/{benchmark_size}...\n")

        # Reinitialize the game for each run
        game = Kulibrat()

        # Assign players again
        black_player = black_player_type(game, ai_depth_black) if black_player_type == MinimaxAI else black_player_type(
            game)
        red_player = red_player_type(game, ai_depth_red) if red_player_type == MinimaxAI else red_player_type(game)

        # Track the number of turns
        turn_count = 0
        winner = None  # Track winner

        while True:
            # -------------------
            # BLACK TURN
            # -------------------
            black_moves = get_legal_moves(game)
            if black_moves:
                chosen = black_player.choose_move(black_moves)
                if chosen is not None:
                    game.make_move(chosen)
                    turn_count += 1
                    if game.scores["B"] >= winning_points:
                        winner = "Black"
                        print(f"Game {game_num}: Black wins after {turn_count} turns!")
                        break
                game.print_board()

            # -------------------
            # RED TURN
            # -------------------
            red_moves = get_legal_moves(game)
            if red_moves:
                chosen = red_player.choose_move(red_moves)
                if chosen is not None:
                    game.make_move(chosen)
                    turn_count += 1
                    if game.scores["R"] >= winning_points:
                        winner = "Red"
                        print(f"Game {game_num}: Red wins after {turn_count} turns!")
                        break
                game.print_board()

            # If both players cannot move, game ends
            if not black_moves and not red_moves:
                print(f"Game {game_num}: Draw! Neither player can move.")
                winner = "Draw"
                break

        results.append((game_num, winner, turn_count))  # Store result

        print("-" * 30)  # Separate games for clarity

    """
    Display Benchmark Results in a Simple Table
    """
    print("\nBenchmark Results:")
    print("=" * 40)
    print(f"{'Game':<8}{'Winner':<10}{'Turns'}")
    print("-" * 40)

    for game, winner, turns in results:
        print(f"{game:<8}{winner:<10}{turns}")

    print("=" * 40)

    # Calculate summary statistics
    black_wins = sum(1 for _, winner, _ in results if winner == "Black")
    red_wins = sum(1 for _, winner, _ in results if winner == "Red")
    draws = sum(1 for _, winner, _ in results if winner == "Draw")
    avg_turns = sum(turns for _, _, turns in results) / benchmark_size

    print("")
    print("Black player type:", black_player_type)
    print("Red player type:", red_player_type)
    if black_player_type == MinimaxAI:
        print("Black player AI difficulty:", ai_depth_black)
    if red_player_type == MinimaxAI:
        print("Red player AI difficulty:", ai_depth_red)
    print("Points to win pr. game: ", winning_points)
    print(f"Black win rate: {black_wins / benchmark_size * 100:.2f}%")
    print(f"Red win rate: {red_wins / benchmark_size * 100:.2f}%")
    print(f"Draw rate: {draws / benchmark_size * 100:.2f}%")
    print(f"Average number of turns per game: {avg_turns:.2f}")

    """
        Generate Dynamic File Name for CSV
        """
    black_player_name = black_player_type.__name__
    red_player_name = red_player_type.__name__

    # Append AI depth to MinimaxAI if selected
    if black_player_type == MinimaxAI:
        black_player_name += f"{ai_depth_black}"
    if red_player_type == MinimaxAI:
        red_player_name += f"{ai_depth_red}"

    filename = f"{black_player_name}_vs_{red_player_name}_{benchmark_size}.csv"

    """
    Create a Subfolder for Results (if not exists)
    """
    results_folder = os.path.join(os.getcwd(), "benchmark_results")
    os.makedirs(results_folder, exist_ok=True)  # Create the folder if it doesn't exist

    """
    Write Results to a CSV File Inside the Subfolder
    """
    csv_path = os.path.join(results_folder, filename)

    with open(csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write Header
        writer.writerow(["Game", "Winner", "Turns"])

        # Write Game Results
        writer.writerows(results)

        # Write Summary Statistics
        writer.writerow([])
        writer.writerow(["Black Wins", black_wins])
        writer.writerow(["Red Wins", red_wins])
        writer.writerow(["Draws", draws])
        writer.writerow(["Average Turns", avg_turns])

    print(f"CSV file saved to: {csv_path}")


def play_game():

    print("Playing...")

    """
    In order to validate the settings: a guick message again
    """
    print("")
    print("You are now ready to play!")
    print("This is the chosen opponent for your game:")
    print("Black player type", black_player_type)
    print("Red player type:", red_player_type)

    if red_player_type == MinimaxAI:
        print("Red player AI difficulty:", ai_depth_red)
    else:
        pass

    print("")

    """
    Now, the settings are used for running the game
    """

    game = Kulibrat()
    black_player = black_player_type(game)

    if red_player_type == MinimaxAI:
        red_player = red_player_type(game, ai_depth_red)  # Set AI depth (increase for smarter AI)
    else:
        red_player = red_player_type(game)

    if winning_points == 1:
        print("The first player to reach", winning_points, "point wins!")
    else:
        print("The first player to reach", winning_points, "points wins!")

    print("")

    """
    The board is printed before the first move
    """

    print("     " + "   ".join(str(i) for i in range(3)))
    print("    --" + "---" * 3)

    # Print each row with lettered row index
    for i, row in enumerate(game.board):
        print(f" {chr(65 + i)} | " + " | ".join(row) + " |")
        print("    --" + "---" * 3)

    print("")

    """
    The pieces available for each player
    """

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

            # Print board at the end of each player's turn
            game.print_board()

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

            # Print board at the end of each player's turn
            game.print_board()

        else:
            print("Red has no moves.")

        # If both players have no moves left, end the game
        if not black_moves and not red_moves:
            print("Neither player can move => game ends.")
            break

    # Final board state
    print("Final board state:")
    game.print_board()
    print(f"Final Score: B={game.scores['B']}  R={game.scores['R']}")

if __name__ == "__main__":

    """
    The settings from setup_game are called
    """

    red_player_type, black_player_type, winning_points, ai_depth_black, ai_depth_red = setup_game()
    if black_player_type is HumanPlayer:
        play_game()
    else:
        benchmark_game()
