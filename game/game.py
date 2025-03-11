# Game loop & player interaction

from game.board import Kulibrat
from game.rules import get_legal_moves

def play_human_vs_human():
    game = Kulibrat()
    while True:
        game.print_board()
        moves = get_legal_moves(game)
        if not moves:
            print(f"Game Over! Final Score: {game.scores}")
            break

        print(f"Legal Moves: {moves}")
        move = input(f"Player {game.current_player}, choose a move: ")
        move = eval(move)  # Convert input string to tuple
        if move in moves:
            game.make_move(move)
        else:
            print("Invalid move, try again!")

if __name__ == "__main__":
    play_human_vs_human()
