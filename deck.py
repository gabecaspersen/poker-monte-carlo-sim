import random
from card import Card

class Deck:
    def __init__(self):
        self.cards = self._generate_deck()
        self.shuffle()

    def _generate_deck(self):
        suits = ["h", "d", "c", "s"]
        values = ["a", "k", "q", "j", "t", "9", "8", "7", "6", "5", "4", "3", "2"]
        return [Card(v + s) for s in suits for v in values]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, n=1):
        if n > len(self.cards):
            raise ValueError("Not enough cards left in the deck.")
        dealt = self.cards[:n]
        self.cards = self.cards[n:]
        return dealt if n > 1 else dealt[0]

    def reset(self):
        self.cards = self._generate_deck()
        self.shuffle()

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f"Deck of {len(self.cards)} cards"
