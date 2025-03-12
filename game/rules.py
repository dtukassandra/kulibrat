def get_legal_moves(board, current_player, players):
    moves = []
    start_row = 0 if current_player == "B" else 3
    opponent = "R" if current_player == "B" else "B"

    # Insert move
    if players[current_player] > 0:
        for col in range(3):
            if board[start_row][col] == " ":
                moves.append(("insert", col))

    # Check for diagonal movement
    for r in range(4):
        for c in range(3):
            if board[r][c] == current_player:
                potential_moves = [(1, -1), (1, 1)] if current_player == "B" else [(-1, -1), (-1, 1)]
                for dr, dc in potential_moves:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 4 and 0 <= nc < 3 and board[nr][nc] == " ":
                        moves.append(("move", (r, c), (nr, nc)))
                    elif (current_player == "B" and r == 3 and nr == 4) or (current_player == "R" and r == 0 and nr == -1):
                        moves.append(("move", (r, c), (nr, nc)))

                # Check for attack moves (piece directly ahead is opponent)
                if r + 1 < 4 and board[r + 1][c] == opponent:
                    moves.append(("attack", (r, c), (r + 1, c)))
                elif r - 1 >= 0 and board[r - 1][c] == opponent:
                    moves.append(("attack", (r, c), (r - 1, c)))

                # Check for jump moves (piece jumps over opponent line)
                if r + 2 < 4 and board[r + 1][c] == opponent and board[r + 2][c] == " ":
                    moves.append(("jump", (r, c), (r + 2, c)))
                elif r - 2 >= 0 and board[r - 1][c] == opponent and board[r - 2][c] == " ":
                    moves.append(("jump", (r, c), (r - 2, c)))
    return moves