# random_agent.py

import random
from game.rules import get_legal_moves

class RandomAI:
    def __init__(self, game):
        """
        Here I'm storing a reference to the game object.
        This AI will only pick a random move from the list
        of valid moves.
        """
        self.game = game

    def choose_move(self, available_moves=None):
        """
        If 'available_moves' is provided, we just pick a random one.
        If it's not provided, we fetch the moves ourselves by calling
        get_legal_moves(...) on the game object.

        Returns:
          - A single move tuple, e.g. ("move", (r,c), (nr,nc))
          - Or None if there are no valid moves.
        """
        # If no move list was passed in, get them from the rules
        if available_moves is None:
            available_moves = get_legal_moves(self.game)

        # If there aren't any moves, return None so we skip
        if not available_moves:
            return None

        # Otherwise pick and return one move at random
        return random.choice(available_moves)
