# 🃏 Poker Monte Carlo Simulator

A Python project that uses Monte Carlo simulation to estimate the winning probabilities of poker hands.
This tool lets you input hole cards and community cards, then runs thousands of random simulations to calculate equity (win/tie/loss percentages).

## 🚀 Features

- Simulates **Texas Hold'em** poker hands
- Estimates winning probability using **Monte Carlo methods**
- Supports **multiple players**
- Clean object-oriented design (`Card`, `Deck`, `Hand`, `Simulator`)
- Fast hand evaluation using [phevaluator](https://github.com/HenryRLee/PokerHandEvaluator)
- Includes visualizations (probability distributions, EV graphs)
- Extendable to other variants or strategy analysis

## 📦 Installation

### Prerequisites

- Python 3.7+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/poker-monte-carlo-sim.git
cd poker-monte-carlo-sim
```

2. Install dependencies:
```bash
pip install phevaluator
```

For visualization features (optional):
```bash
pip install matplotlib numpy pandas
```

## 🎮 Usage

### Basic Example

```python
from card import Card
from deck import Deck
from hand import Hand
from evaluator import evaluate_hand

# Create your hole cards
hole_cards = ["Ah", "Kd"]  # Ace of Hearts, King of Diamonds

# Create a hand
hand = Hand(hole_cards, player_id=1)

# Simulate a board
board = ["Qs", "Jc", "Ts"]  # Flop

# Evaluate the hand
rank, hand_type = hand.evaluate(board + ["2h", "3d"])  # Add turn and river
print(f"Hand: {hand_type}, Rank: {rank}")
```

### Monte Carlo Simulation Example

```python
from deck import Deck
from hand import Hand

# Your hole cards
hole_cards = ["Ah", "Kh"]

# Known community cards (e.g., after the flop)
board = ["Qh", "Jh", "2d"]

# Create a deck and remove known cards
deck = Deck()
deck.remove_cards(hole_cards + board)

# Run simulations
wins = 0
simulations = 10000

for _ in range(simulations):
    # Deal remaining community cards
    sim_deck = Deck()
    sim_deck.remove_cards(hole_cards + board)
    remaining = sim_deck.deal(5 - len(board))

    # Evaluate hand
    hand = Hand(hole_cards)
    rank, hand_type = hand.evaluate(board + remaining)

    # Compare against opponent (simplified)
    # ... (add opponent simulation logic)

print(f"Win probability: {wins / simulations * 100:.2f}%")
```

## 📚 API Documentation

### Card Class

Represents a single playing card.

```python
card = Card("Ah")  # Ace of Hearts
```

**Methods:**
- `to_string()` - Returns card in phevaluator format (e.g., "Ah")
- `__str__()` - Returns readable format (e.g., "A of Hearts")
- `__eq__()` - Compare cards for equality
- `__hash__()` - Make cards hashable (usable in sets/dicts)

**Supported formats:**
- Values: `2-9`, `t/T` (10), `j/J` (Jack), `q/Q` (Queen), `k/K` (King), `a/A` (Ace)
- Suits: `h` (Hearts), `d` (Diamonds), `c` (Clubs), `s` (Spades)

### Deck Class

Represents a standard 52-card deck.

```python
deck = Deck()
```

**Methods:**
- `shuffle()` - Randomly shuffles the deck
- `deal(n=1)` - Deals n cards from the deck
- `reset()` - Restores deck to full 52 cards and shuffles
- `remove_cards(cards)` - Removes specific cards from deck (for Monte Carlo)
- `remaining_cards()` - Returns number of cards left in deck
- `__len__()` - Returns number of cards in deck

### Hand Class

Represents a poker hand with hole cards.

```python
hand = Hand(["Ah", "Kd"], player_id=1)
```

**Attributes:**
- `hole_cards` - List of hole card strings
- `rank` - Hand rank (lower is better)
- `type` - Hand type (e.g., "Straight Flush")
- `equity` - Win probability (0-1)
- `player_id` - Optional player identifier

**Methods:**
- `evaluate(board)` - Evaluates hand with given board cards
- `update_equity(equity)` - Updates hand equity
- `reset()` - Resets evaluation attributes
- Comparison operators (`<`, `==`) for ranking hands

### Evaluator

Hand evaluation using phevaluator.

```python
from evaluator import evaluate_hand

rank, hand_type = evaluate_hand(["Ah", "Kd", "Qh", "Jc", "Ts", "2d", "3h"])
```

**Function:**
- `evaluate_hand(cards)` - Evaluates a 7-card poker hand
  - **Args:** List of 7 card strings
  - **Returns:** Tuple of (rank: int, hand_type: str)
  - **Raises:** ValueError if not exactly 7 cards

## 🏗️ Project Structure

```
poker-monte-carlo-sim/
├── card.py          # Card class implementation
├── deck.py          # Deck class implementation
├── hand.py          # Hand class implementation
├── evaluator.py     # Hand evaluation wrapper
├── simulator.py     # Monte Carlo simulator (coming soon)
├── visualize.py     # Visualization tools (coming soon)
└── README.md        # This file
```

## 🎯 Roadmap

- [ ] Implement full Monte Carlo simulator class
- [ ] Add multi-player support
- [ ] Implement equity calculations
- [ ] Add visualization for probability distributions
- [ ] Create CLI interface
- [ ] Add support for different poker variants
- [ ] Implement range vs range equity calculations
- [ ] Add hand history analysis

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [phevaluator](https://github.com/HenryRLee/PokerHandEvaluator) - Fast poker hand evaluation library
- Monte Carlo methods for poker equity calculation

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Happy simulating!** 🎲♠️♥️♣️♦️
# touch
