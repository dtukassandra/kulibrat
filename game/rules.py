# rules.py

def get_legal_moves(game):
    """
    This function gathers all possible moves the current player can make.
    It just combines the lists from each helper function below.
    For example, the returned moves might look like:
      [("insert", 2),
       ("attack", (1,0), (2,0)),
       ("move", (0,2), (1,3)), ...]
    """
    moves = []
    moves.extend(_get_insert_moves(game))
    moves.extend(_get_diagonal_moves(game))
    moves.extend(_get_attack_moves(game))
    moves.extend(_get_jump_moves(game))
    return moves


def _get_insert_moves(game):
    """
    Checks if the current player can insert a piece in their start row.
    - If the player still has pieces left in reserve,
    - And if there is an empty space ('.') in their start row,
    we create a move like ("insert", col).
    """
    moves = []
    current_player = game.current_player
    board = game.board

    # If the player has pieces in reserve...
    if game.players[current_player] > 0:
        # Black inserts at row 0, Red inserts at row 3
        start_row = 0 if current_player == "B" else 3
        # Check each column in that row
        for col in range(3):
            if board[start_row][col] == " ":
                # This means it's a valid insert move
                moves.append(("insert", col))

    return moves


def _get_diagonal_moves(game):
    """
    Diagonal forward moves:
      - For Black: row r -> r+1, col c +/- 1
      - For Red:   row r -> r-1, col c +/- 1

    If the destination is off the board, we treat that as ("jump_score", (r,c)),
    which gives the player a point. If it's on the board and empty, we return
    ("move", (r,c), (nr,nc)).
    """
    moves = []
    current_player = game.current_player
    board = game.board

    # Black moves "down" (row+1), Red moves "up" (row-1)
    row_step = 1 if current_player == "B" else -1

    for r in range(4):
        for c in range(3):
            if board[r][c] == current_player:
                # Try going diagonally left or right
                for dc in [-1, +1]:
                    nr = r + row_step
                    nc = c + dc
                    # If nr is outside [0..3], the piece "scores" off the board
                    if nr < 0 or nr > 3:
                        moves.append(("jump_score", (r,c)))
                    else:
                        # If it's still on the board, check if the spot is empty
                        if 0 <= nc < 3 and board[nr][nc] == " ":
                            moves.append(("move", (r,c), (nr,nc)))
    return moves


def _get_attack_moves(game):
    """
    Attack happens if the opponent is directly in front of our piece:
      - Black sees "in front" as (r+1, c)
      - Red sees "in front" as (r-1, c)
    If that square contains the opponent, we can return ("attack", (r,c), (nr,nc)).
    """
    moves = []
    current_player = game.current_player
    opponent = "R" if current_player == "B" else "B"
    board = game.board

    row_step = 1 if current_player == "B" else -1

    for r in range(4):
        for c in range(3):
            if board[r][c] == current_player:
                nr = r + row_step
                nc = c
                # Make sure we're still within the board bounds
                if 0 <= nr < 4:
                    # If there's an opponent piece there, we can attack
                    if board[nr][nc] == opponent:
                        moves.append(("attack", (r,c), (nr,nc)))

    return moves


def _get_jump_moves(game):
    """
    Jump lets you leap over a line (1 to 3) of consecutive opponent pieces
    directly behind your piece. The 'behind' direction depends on who you are:
      - Black: behind is row+something
      - Red: behind is row-something

    If the square after that line is off the board, it's ("jump_score", (r,c));
    If it's on the board and empty, it's ("jump", (r,c), (nr,nc)).
    The line has to be full of opponent pieces, no gaps or friendly pieces allowed.
    """
    moves = []
    current_player = game.current_player
    opponent = "R" if current_player == "B" else "B"
    board = game.board
    row_step = 1 if current_player == "B" else -1

    for r in range(4):
        for c in range(3):
            if board[r][c] == current_player:
                # Check jump lines of length 1, 2, or 3
                for length in [1,2,3]:
                    final_r = r + (length+1)*row_step

                    # We want to see if the squares r+i*row_step all have the opponent
                    contiguous = True
                    for i in range(1, length+1):
                        check_r = r + i*row_step
                        # If we jump out of the board, it's not a valid line
                        if not (0 <= check_r < 4):
                            contiguous = False
                            break
                        if board[check_r][c] != opponent:
                            contiguous = False
                            break

                    if contiguous:
                        # If final_r is off the board => "jump_score"
                        if not (0 <= final_r < 4):
                            moves.append(("jump_score", (r,c)))
                        else:
                            # If it's on the board, check if empty => "jump"
                            if board[final_r][c] == " ":
                                moves.append(("jump", (r,c), (final_r,c)))

    return moves
