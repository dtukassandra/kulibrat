#Game rules, legal moves

def get_legal_moves(game):
    #Returns all legal moves for the current player in a 4x3 board.
    moves = []
    start_row = 0 if game.current_player == "B" else 3  # Black inserts from row 0, Red from row 3

    # Insert piece (if available)
    if game.players[game.current_player] > 0:
        for col in range(3):
            if game.board[start_row][col] == ".":
                moves.append(("insert", col))

    # Check for diagonal moves
    for r in range(4):
        for c in range(3):
            if game.board[r][c] == game.current_player:
                # Determine diagonal movement direction
                if game.current_player == "B":
                    potential_moves = [(-1, -1), (-1, 1)]  # Moves up diagonally
                else:
                    potential_moves = [(1, -1), (1, 1)]   # Moves down diagonally

                for dr, dc in potential_moves:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 4 and 0 <= nc < 3 and game.board[nr][nc] == ".":
                        moves.append(("move", (r, c), (nr, nc)))

    return moves
