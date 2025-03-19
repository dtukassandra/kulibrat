# board.py

class Kulibrat:
    def __init__(self):
        """
        Here I'm setting up the board as a 4x3 grid.
        Each spot can be:
          'B' for Black
          'R' for Red
          '.' for empty
        At the start, every square is empty ('.').
        """
        self.board = [["." for _ in range(3)] for _ in range(4)]

        """
        players: tracks how many pieces each side (B or R) has
        "in reserve" (not yet placed on the board). The official rules
        say each player starts with 4 pieces off-board.
        """
        self.players = {"B": 4, "R": 4}

        """
        scores: tracks how many points each side has earned.
        A point is gained when a piece moves off the board (jump_score).
        """
        self.scores = {"B": 0, "R": 0}

        """
        current_player: we let Black start the game by default.
        """
        self.current_player = "B"

    def print_board(self):
        """
        Display the current state of the game:
         - Show whose turn it is
         - Print the board
         - Show scores and pieces in reserve
        """
        print(f"Current Player: {self.current_player}")

        # Print board normally with B and R for players

        # Print column headers
        print("     " + "   ".join(str(i) for i in range(3)))
        print("    --" + "---" * 3)

        # Print each row with lettered row index
        for i, row in enumerate(self.board):
            print(f" {chr(65 + i)} | " + " | ".join(row) + " |")
            print("    --" + "---" * 3)

        # Display scores and pieces left for each player
        print(f"Scores: B={self.scores['B']}, R={self.scores['R']}")
        print(f"Pieces in reserve: B={self.players['B']} R={self.players['R']}")
        print("-" * 20)

    def make_move(self, move):
        """
        Applies a chosen move to the board. A move can be:
          ("insert", col)
          ("move", (r,c), (nr,nc))
          ("attack", (r,c), (nr,nc))
          ("jump", (r,c), (nr,nc))
          ("jump_score", (r,c))

        The 'kind' is the first element in the tuple, like 'insert' or 'attack'.
        Then we interpret the rest of the tuple accordingly.
        """
        kind = move[0]
        opponent = "R" if self.current_player == "B" else "B"

        if kind == "insert":
            # For an insert move, we only store ("insert", col)
            col = move[1]
            # Black inserts at row 0, Red at row 3
            row = 0 if self.current_player == "B" else 3
            # Place the current player's piece in that column
            self.board[row][col] = self.current_player
            # Subtract one piece from that player's reserve
            self.players[self.current_player] -= 1

        elif kind == "move":
            # For a normal diagonal move, we have ("move", (r,c), (nr,nc))
            _, (r, c), (nr, nc) = move
            # Move the piece on the board
            self.board[nr][nc] = self.board[r][c]
            self.board[r][c] = "."

        elif kind == "attack":
            # For an attack, it's ("attack", (r,c), (nr,nc))
            _, (r, c), (nr, nc) = move
            # The opponent's piece that was attacked goes back to their reserve
            self.players[opponent] += 1
            # Then the current player's piece occupies that square
            self.board[nr][nc] = self.board[r][c]
            self.board[r][c] = "."

        elif kind == "jump":
            # For jumping over a contiguous line of opponent pieces,
            # we land in (nr,nc), e.g. ("jump", (r,c), (nr,nc))
            _, (r, c), (nr, nc) = move
            self.board[nr][nc] = self.board[r][c]
            self.board[r][c] = "."

        elif kind == "jump_score":
            # For jumping off the board, e.g. ("jump_score", (r,c))
            _, (r, c) = move
            # The player gains a point...
            self.scores[self.current_player] += 1
            # ...and that piece returns to their reserve
            self.players[self.current_player] += 1
            # Remove it from the board
            self.board[r][c] = "."

        else:
            # If we encounter a move type we didn't code for
            print(f"Unknown move type: {kind}")
            return

        # Finally, we switch turns. If it was B, it becomes R; if it was R, it becomes B.
        self.current_player = opponent
