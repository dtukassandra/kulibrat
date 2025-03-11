#Game logic, board representation

class Kulibrat:
    def __init__(self):
        # initialize a 3x4 board with empty spaces
        self.board = [["." for _ in range(3)] for _ in range(3)]
        self.players = {"B": 4, "R": 4}
        self.scores = {"B": 0, "R": 0}
        self.current_player = "B"

    def print_board(self):
        # display the board
        for row in self.board:
            print(" ".join(row))
        print(f"Scores: Black={self.scores['B']}, Red={self.scores['R']}\n")

hej

commit