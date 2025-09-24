import numpy as np
import pandas as pd
import matplotlib as plt
from enum import Enum

 
class Card:
    # Mapping from shorthand to full name
    suit_map = {
        "h": "Hearts",
        "d": "Diamonds",
        "c": "Clubs",
        "s": "Spades"
    }
    value_map = {
        "a": "A",
        "k": "K",
        "q": "Q",
        "j": "J",
        "t": "10",   # allow 't' for ten
        "2": "2", "3": "3", "4": "4", "5": "5",
        "6": "6", "7": "7", "8": "8", "9": "9"
    }

    def __init__(self, input_str: str):
        input_str = input_str.strip().lower()  # normalize

        if len(input_str) < 2:
            raise ValueError("Card input must have value and suit (e.g. 'kh', '7s')")

        value_char, suit_char = input_str[:-1], input_str[-1]

        if value_char not in self.value_map:
            raise ValueError(f"Invalid card value: {value_char}")
        if suit_char not in self.suit_map:
            raise ValueError(f"Invalid card suit: {suit_char}")

        self.value = self.value_map[value_char]
        self.suit = self.suit_map[suit_char]

    def __repr__(self):
        return f"{self.value} of {self.suit}"
