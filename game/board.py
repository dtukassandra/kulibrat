#Game logic, board representation

class Kulibrat:
    def __init__(self):
        #Initializes a 4x3 board with empty spaces. Players insert from row 0 (Black) and row 3 (Red)
        self.board = [["." for _ in range(3)] for _ in range(4)]
        self.players = {"B": 4, "R": 4}  # Available pieces for each player
        self.scores = {"B": 0, "R": 0}   # Score tracking
        self.current_player = "B"  # Black starts

    def print_board(self):
        #Displays the current board state.
        print(f"\nCurrent Player: {self.current_player}")
        for row in self.board:
            print(" ".join(row))
        print(f"Scores: Black={self.scores['B']}, Red={self.scores['R']}\n")
