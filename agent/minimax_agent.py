# minimax_agent.py

from game.rules import get_legal_moves
import copy

class MinimaxAI:
    def __init__(self, game, depth=3):
        """
        Initializes the Minimax agent.
        :param game: Reference to the game object.
        :param depth: Maximum depth for the Minimax search.
        """
        self.game = game
        self.depth = depth

    def choose_move(self, available_moves=None):
        """
        Returns the best move based on Minimax.
        :param available_moves: A list of available moves.
        :return: The best move tuple.
        """
        if available_moves is None:
            available_moves = get_legal_moves(self.game)
        if not available_moves:
            return None  # No moves possible

        best_move = None
        best_score = float('-inf') #starting with the lowest score possible

        for move in available_moves:
            # Simulate the move by copying the board
            game_copy = copy.deepcopy(self.game)
            game_copy.make_move(move)

            # Check if this move is a goal scoring move
            if game_copy.scores["R"] > self.game.scores["R"]:
                return move  # Immediate scoring move, take it!

            # Get the Minimax score
            score = self._minimax(game_copy, self.depth, False)

            # Pick the move with the highest score
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, game, depth, is_maximizing):
        """
        The recursive Minimax function.
        :param game: A simulated game state.
        :param depth: The remaining depth to search.
        :param is_maximizing: Boolean indicating if it's the maximizing player's turn.
        :return: A heuristic score of the board state.
        """
        # Base cases: If game is over or depth is 0, return the evaluation
        if depth == 0 or not get_legal_moves(game):
            return self._evaluate_board(game)

        # Get available moves
        moves = get_legal_moves(game)

        if is_maximizing:
            max_eval = float('-inf')
            for move in moves:
                game_copy = copy.deepcopy(game)
                game_copy.make_move(move)
                eval_score = self._minimax(game_copy, depth - 1, False)
                max_eval = max(max_eval, eval_score)
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                game_copy = copy.deepcopy(game)
                game_copy.make_move(move)
                eval_score = self._minimax(game_copy, depth - 1, True)
                min_eval = min(min_eval, eval_score)
            return min_eval

    def _evaluate_board(self, game):
        """
        Evaluates the board state for Minimax.

        New Criteria:
        - Score difference (primary goal, since scoring wins the game)
        - Attack potential (prioritize capturing opponent pieces)
        - Jump potential (prioritize jumps, since they can score)
        - Piece advancement (encourage moving forward)
        - Mobility (avoid getting trapped)
        - Blocking opponent's jumps (reduce opponent options)
        """

        # Weights for different factors
        score_weight = 35  # Scoring is most important
        attack_weight = 10  # Higher priority on attacking opponent pieces
        jump_weight = 12  # Slightly below scoring, but still important
        position_weight = 2  # Still rewards advancement but less than before
        mobility_weight = 1  # Keeps options open
        block_weight = 5  # Discourage opponent movement

        # Score difference (main objective)
        score_eval = (game.scores["B"] - game.scores["R"]) * score_weight

        position_eval = 0
        attack_eval = 0
        jump_eval = 0
        mobility_eval = 0
        block_eval = 0

        black_moves = get_legal_moves(game)
        red_moves = get_legal_moves(game)

        for r in range(4):
            for c in range(3):
                piece = game.board[r][c]

                if piece == "R":  # Red (our AI's pieces)
                    position_eval += (3 - r) * position_weight  # Moving forward is good

                    # Check if this piece is in a position to attack Red
                    if (r + 1 < 4) and game.board[r + 1][c] == "B":
                        attack_eval += attack_weight  # Encourage attacking Red

                    # Check if this piece can perform a jump move
                    if (r + 2 < 4) and game.board[r + 1][c] == "B" and game.board[r + 2][c] == ".":
                        jump_eval += jump_weight  # Encourage jumps over enemy

                elif piece == "B":  # black (opponent)
                    position_eval -= r * position_weight  # Encourage moving forward

                    # Check if this piece is in a position to attack Black
                    if (r - 1 >= 0) and game.board[r - 1][c] == "R":
                        attack_eval -= attack_weight  # Discourage being attacked

                    # Check if this piece can perform a jump move
                    if (r - 2 >= 0) and game.board[r - 1][c] == "R" and game.board[r - 2][c] == ".":
                        jump_eval -= jump_weight  # Discourage opponent jumps

        # Blocking opponent: If Black has many moves and Red has few, it's good for Black
        block_eval = (len(black_moves) - len(red_moves)) * block_weight

        # Mobility: Encourage keeping options open
        mobility_eval += len(black_moves) * mobility_weight
        mobility_eval -= len(red_moves) * mobility_weight  # If Red has many moves, that's bad for Black

        # Final heuristic score
        return score_eval + attack_eval + jump_eval + position_eval + mobility_eval + block_eval
