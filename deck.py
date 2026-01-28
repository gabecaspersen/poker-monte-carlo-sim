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

    def remove_cards(self, cards_to_remove):
        """
        Remove specific cards from the deck.
        Useful for Monte Carlo simulation when some cards are already known.

        Args:
            cards_to_remove: List of Card objects or list of string representations
        """
        if not cards_to_remove:
            return

        # Convert to Card objects if strings are provided
        if isinstance(cards_to_remove[0], str):
            cards_to_remove = [Card(c) for c in cards_to_remove]

        # Remove cards from deck
        self.cards = [card for card in self.cards if card not in cards_to_remove]

    def remaining_cards(self):
        """Returns the number of cards remaining in the deck"""
        return len(self.cards)

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f"Deck({len(self.cards)} cards remaining)"
