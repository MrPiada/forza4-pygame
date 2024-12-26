import random


class RandomStrategy:
    def __init__(self):
        self.name = "Random Strategy"

    def play(self, board):
        return random.choice(board.get_valid_moves())

    def __str__(self):
        return self.name
