class Board:
    def __init__(self):
        # Initialize a 4x3 board with empty spaces
        self.board = [[" " for _ in range(3)] for _ in range(4)]
        self.scores = {"B": 0, "R": 0}  # Move scores inside the board class
        self.win_score = 5  # Define winning score

    def print_board(self):
        # Print column headers
        print("     " + "   ".join(str(i) for i in range(3)))
        print("    --" + "---" * 3)

        # Print each row with lettered row index
        for i, row in enumerate(self.board):
            print(f" {chr(65 + i)} | " + " | ".join(row) + " |")
            print("    --" + "---" * 3)

        # Print scores
        print(f"Scores: Black={self.scores['B']}, Red={self.scores['R']}\n")

    def update_board(self, move, current_player, players):
        if move[0] == "insert":
            col = move[1]
            row = 0 if current_player == "B" else 3
            self.board[row][col] = current_player
        elif move[0] == "move":
            r, c, nr, nc = move[1][0], move[1][1], move[2][0], move[2][1]
            if self.board[r][c] == current_player:
                # Check if the piece is moving off the board diagonally from the opponent's start row
                if (current_player == "B" and r == 3 and nr == 4) or (current_player == "R" and r == 0 and nr == -1):
                    self.scores[current_player] += 1
                    players[current_player] += 1  # Return the piece to the pool
                    self.board[r][c] = " "  # Remove the piece from the board
                elif 0 <= nr < 4 and 0 <= nc < 3 and self.board[nr][nc] == " ":
                    self.board[nr][nc] = self.board[r][c]
                    self.board[r][c] = " "
        elif move[0] == "attack":
            r, c, nr, nc = move[1][0], move[1][1], move[2][0], move[2][1]
            if self.board[r][c] == current_player and self.board[nr][nc] != " ":
                self.board[nr][nc] = current_player
                self.board[r][c] = " "
                players["R" if current_player == "B" else "B"] += 1  # Return opponent's piece
        elif move[0] == "jump":
            r, c, nr, nc = move[1][0], move[1][1], move[2][0], move[2][1]
            if self.board[r][c] == current_player:
                if (current_player == "B" and nr == 4) or (current_player == "R" and nr == -1):
                    self.scores[current_player] += 1
                    players[current_player] += 1  # Return the piece to the pool
                    self.board[r][c] = " "  # Remove the piece from the board
                elif 0 <= nr < 4 and 0 <= nc < 3:
                    self.board[nr][nc] = self.board[r][c]
                    self.board[r][c] = " "