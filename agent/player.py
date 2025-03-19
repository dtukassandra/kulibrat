# player.py

class HumanPlayer:

    def __init__(self, game):
        """
        I'm saving a reference to the main game object
        because I might want to know which player's turn it is,
        or access other game details if needed.
        """
        self.game = game


    def choose_move(self, available_moves):
        """
        This method is where a human user picks from a list of valid moves.
        - First, we print each move (with describe_move(...) to make it easier to read).
        - Then we ask the user for an index.
        - The user can also type 'exit' to quit the game.
        - If a valid index is chosen, we return the corresponding move tuple.
        """
        if not available_moves:
            return None  # If there's no valid move, do nothing.

        # Print each move for the user, giving a short description.
        for i, move in enumerate(available_moves):
            print(f"{i}: {describe_move(move)}")

        # Keep asking for a number or "exit" until we get a valid input.
        while True:
            choice = input(
                f"Player {self.game.current_player}, pick a move [0..{len(available_moves) - 1}] or type 'exit' to quit: "
            )

            # Allow the user to quit the game by typing 'exit'
            if choice.lower() == "exit":
                print("Exiting the game. Thanks for playing!")
                exit()  # Immediately terminates the game

            try:
                idx = int(choice)
                if 0 <= idx < len(available_moves):
                    # Return the actual move tuple if the index is valid.
                    return available_moves[idx]
                else:
                    print("Invalid index. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number or 'exit' to quit.")

def describe_move(move):
    """
    This helper function takes a move tuple (like ("insert", 2) or
    ("move", (1,1), (2,2))) and returns a human-friendly string.
    That way, people can see exactly what each move does before choosing.
    """
    kind = move[0]

    if kind == "insert":
        col = move[1]
        return f"Insert at column {col}"

    elif kind == "move":
        # move is something like ("move", (r,c), (nr,nc))
        _, (r, c), (nr, nc) = move
        return f"Move from ({r},{c}) to ({nr},{nc})"

    elif kind == "attack":
        # ("attack", (r,c), (nr,nc))
        _, (r, c), (nr, nc) = move
        return f"Attack from ({r},{c}) to ({nr},{nc})"

    elif kind == "jump":
        # ("jump", (r,c), (nr,nc))
        _, (r, c), (nr, nc) = move
        return f"Jump from ({r},{c}) to ({nr},{nc})"

    elif kind == "jump_score":
        # ("jump_score", (r,c))
        _, (r, c) = move
        return f"Score jump from ({r},{c})"

    else:
        # Fallback, in case something new appears.
        return str(move)
