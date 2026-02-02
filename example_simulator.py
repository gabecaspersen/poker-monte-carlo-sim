"""
Example usage of the PokerSimulator class.

Demonstrates various scenarios:
1. Pre-flop equity calculation
2. Flop equity calculation
3. Turn equity calculation
4. River equity calculation
"""

from card import Card
from hand import Hand
from simulator import PokerSimulator


def example_preflop():
    """Calculate pre-flop equity for two players."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Pre-flop Equity")
    print("="*60)

    # Player 0: Pocket Aces
    player0 = Hand([Card('Ah'), Card('As')])

    # Player 1: Pocket Kings
    player1 = Hand([Card('Kh'), Card('Ks')])

    # No community cards yet
    sim = PokerSimulator(
        players=2,
        community_cards=[],
        player_hands=[player0, player1],
        num_simulations=10000
    )

    sim.run_simulation()
    sim.print_results()


def example_flop():
    """Calculate equity after the flop."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Flop Equity")
    print("="*60)

    # Player 0: A♥ K♥ (flush draw + overcards)
    player0 = Hand([Card('Ah'), Card('Kh')])

    # Player 1: Q♠ Q♣ (pocket queens)
    player1 = Hand([Card('Qs'), Card('Qc')])

    # Flop: 9♥ 7♥ 2♠
    community_cards = [Card('9h'), Card('7h'), Card('2s')]

    sim = PokerSimulator(
        players=2,
        community_cards=community_cards,
        player_hands=[player0, player1],
        num_simulations=10000
    )

    sim.run_simulation()
    sim.print_results()


def example_turn():
    """Calculate equity on the turn."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Turn Equity")
    print("="*60)

    # Player 0: 8♠ 7♠ (straight draw)
    player0 = Hand([Card('8s'), Card('7s')])

    # Player 1: A♦ A♣ (pocket aces)
    player1 = Hand([Card('Ad'), Card('Ac')])

    # Board: 9♥ 6♣ 2♦ 5♠
    community_cards = [Card('9h'), Card('6c'), Card('2d'), Card('5s')]

    sim = PokerSimulator(
        players=2,
        community_cards=community_cards,
        player_hands=[player0, player1],
        num_simulations=10000
    )

    sim.run_simulation()
    sim.print_results()


def example_three_players():
    """Calculate equity for three players on the flop."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Three-Player Flop")
    print("="*60)

    # Player 0: A♠ K♠
    player0 = Hand([Card('As'), Card('Ks')])

    # Player 1: Q♥ Q♦
    player1 = Hand([Card('Qh'), Card('Qd')])

    # Player 2: J♣ T♣
    player2 = Hand([Card('Jc'), Card('Tc')])

    # Flop: K♥ Q♠ 9♦
    community_cards = [Card('Kh'), Card('Qs'), Card('9d')]

    sim = PokerSimulator(
        players=3,
        community_cards=community_cards,
        player_hands=[player0, player1, player2],
        num_simulations=10000
    )

    sim.run_simulation()
    sim.print_results()


def example_with_dataframe():
    """Example showing DataFrame output (if pandas available)."""
    print("\n" + "="*60)
    print("EXAMPLE 5: DataFrame Output")
    print("="*60)

    player0 = Hand([Card('As'), Card('Ad')])
    player1 = Hand([Card('Kh'), Card('Kd')])
    player2 = Hand([Card('Qs'), Card('Qd')])

    community_cards = [Card('Ah'), Card('7c'), Card('2s')]

    sim = PokerSimulator(
        players=3,
        community_cards=community_cards,
        player_hands=[player0, player1, player2],
        num_simulations=5000
    )

    sim.run_simulation()

    # Try to get DataFrame
    df = sim.get_results_dataframe()
    if df is not None:
        print("\nResults as DataFrame:")
        print(df.to_string(index=False))
    else:
        print("\nPandas not available - install with: pip install pandas")
        sim.print_results()


def example_using_strings():
    """Example showing you can use string card notation."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Using String Card Notation")
    print("="*60)

    # Can use strings instead of Card objects
    player0 = Hand([Card('Ah'), Card('Kh')])
    player1 = Hand([Card('Qs'), Card('Qd')])

    # Community cards as strings
    community_cards = ['9h', '7h', '2s']

    sim = PokerSimulator(
        players=2,
        community_cards=community_cards,
        player_hands=[player0, player1],
        num_simulations=10000
    )

    sim.run_simulation()

    # Get equity data as dict
    equity = sim.calculate_equity()

    print(f"\nPlayer 0 Equity: {equity[0]['equity']:.1%}")
    print(f"Player 1 Equity: {equity[1]['equity']:.1%}")


if __name__ == "__main__":
    # Run all examples
    example_preflop()
    example_flop()
    example_turn()
    example_three_players()
    example_with_dataframe()
    example_using_strings()

    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)
