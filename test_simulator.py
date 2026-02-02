"""
Standalone test for PokerSimulator that doesn't rely on evaluator.py imports.
"""

from card import Card
from deck import Deck
from simulator import PokerSimulator


# Simple Hand class for testing (doesn't depend on evaluator.py)
class SimpleHand:
    def __init__(self, hole_cards):
        self.hole_cards = hole_cards
        self.rank = None
        self.type = None
        self.equity = None
        self.player_id = None


def test_preflop():
    """Test pre-flop equity: AA vs KK"""
    print("\n" + "="*60)
    print("TEST 1: Pre-flop AA vs KK")
    print("="*60)

    player0 = SimpleHand([Card('Ah'), Card('As')])
    player1 = SimpleHand([Card('Kh'), Card('Ks')])

    sim = PokerSimulator(
        players=2,
        community_cards=[],
        player_hands=[player0, player1],
        num_simulations=10000
    )

    print("Running simulation...")
    sim.run_simulation()
    sim.print_results()

    equity = sim.calculate_equity()
    print(f"\nExpected: AA should have ~82% equity")
    print(f"Actual: AA has {equity[0]['equity']:.1%} equity")


def test_flop_with_draw():
    """Test flop equity with flush draw"""
    print("\n" + "="*60)
    print("TEST 2: Flush Draw vs Overpair")
    print("="*60)

    player0 = SimpleHand([Card('Ah'), Card('Kh')])
    player1 = SimpleHand([Card('Qs'), Card('Qc')])
    community = [Card('9h'), Card('7h'), Card('2s')]

    sim = PokerSimulator(
        players=2,
        community_cards=community,
        player_hands=[player0, player1],
        num_simulations=10000
    )

    print("Running simulation...")
    sim.run_simulation()
    sim.print_results()


def test_three_players():
    """Test three-player scenario"""
    print("\n" + "="*60)
    print("TEST 3: Three Players")
    print("="*60)

    player0 = SimpleHand([Card('As'), Card('Ks')])
    player1 = SimpleHand([Card('Qh'), Card('Qd')])
    player2 = SimpleHand([Card('Jc'), Card('Tc')])
    community = [Card('Kh'), Card('Qs'), Card('9d')]

    sim = PokerSimulator(
        players=3,
        community_cards=community,
        player_hands=[player0, player1, player2],
        num_simulations=10000
    )

    print("Running simulation...")
    sim.run_simulation()
    sim.print_results()


def test_turn_equity():
    """Test equity on the turn"""
    print("\n" + "="*60)
    print("TEST 4: Turn - Straight Draw vs Overpair")
    print("="*60)

    player0 = SimpleHand([Card('8s'), Card('7s')])
    player1 = SimpleHand([Card('Ad'), Card('Ac')])
    community = [Card('9h'), Card('6c'), Card('2d'), Card('5s')]

    sim = PokerSimulator(
        players=2,
        community_cards=community,
        player_hands=[player0, player1],
        num_simulations=10000
    )

    print("Running simulation...")
    sim.run_simulation()
    sim.print_results()


def test_using_string_cards():
    """Test using string notation for cards"""
    print("\n" + "="*60)
    print("TEST 5: Using String Card Notation")
    print("="*60)

    player0 = SimpleHand([Card('Ah'), Card('Ad')])
    player1 = SimpleHand([Card('Kh'), Card('Kd')])

    # Mix of Card objects and strings
    community = ['Ac', '7c', '2s']

    sim = PokerSimulator(
        players=2,
        community_cards=community,
        player_hands=[player0, player1],
        num_simulations=5000
    )

    print("Running simulation...")
    sim.run_simulation()

    equity = sim.calculate_equity()
    print(f"\nPlayer 0 (AAA): {equity[0]['equity']:.1%} equity")
    print(f"Player 1 (KK):  {equity[1]['equity']:.1%} equity")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("POKER SIMULATOR TESTS")
    print("="*60)

    test_preflop()
    test_flop_with_draw()
    test_three_players()
    test_turn_equity()
    test_using_string_cards()

    print("\n" + "="*60)
    print("ALL TESTS COMPLETED!")
    print("="*60)
