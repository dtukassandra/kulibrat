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
        :param available_moves: A list of available moves (optional).
        :return: The best move tuple.
        """
        if available_moves is None:
            available_moves = get_legal_moves(self.game)
        if not available_moves:
            return None  # No moves possible

        best_move = None
        best_score = float('-inf')

        for move in available_moves:
            # Simulate the move
            game_copy = copy.deepcopy(self.game)
            game_copy.make_move(move)

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
        :param game: A simulated game state.
        :return: A heuristic score.
        """
        # Basic heuristic: Difference in scores
        return game.scores["B"] - game.scores["R"]
