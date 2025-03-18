from game.board import Kulibrat
from game.rules import get_legal_moves


def play_human_vs_human():
    board = Kulibrat()
    players = {"B": 4, "R": 4}
    current_player = "B"

    while True:
        board.print_board()
        if board.scores["B"] >= board.win_score or board.scores["R"] >= board.win_score:
            print(f"Game Over! {current_player} wins with {board.scores[current_player]} points!")
            break

        moves = get_legal_moves(board.board, current_player, players)

        if not moves and players[current_player] == 0:
            print(f"No moves for {current_player}. {('B' if current_player == 'R' else 'R')} gets an extra turn!")
            current_player = "B" if current_player == "R" else "R"
            continue

        print("Legal Moves:")
        for i, move in enumerate(moves):
            print(f"{i}: {move}")

        try:
            move_index = int(input(f"Player {current_player}, choose a move by typing the corresponding number: "))
            if 0 <= move_index < len(moves):
                board.update_board(moves[move_index], current_player, players)
                if moves[move_index][0] == "insert":
                    players[current_player] -= 1
                current_player = "B" if current_player == "R" else "R"
            else:
                print("Invalid selection, try again!")
        except ValueError:
            print("Invalid input, enter a number!")


if __name__ == "__main__":
    play_human_vs_human()

