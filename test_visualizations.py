"""
Test and demonstration file for PokerSimulator visualization features.

Demonstrates:
1. Equity bar charts
2. Outcome distribution (stacked bars)
3. Individual pie charts
4. Equity convergence over simulations
5. Batch generation of all visualizations
"""

from card import Card
from simulator import PokerSimulator
import os


class SimpleSimpleHand:
    """Simple hand class for testing."""
    def __init__(self, hole_cards):
        self.hole_cards = hole_cards


def demo_two_player_preflop():
    """Demo: Two player pre-flop visualization"""
    print("\n" + "="*70)
    print("DEMO 1: Two Player Pre-flop (AA vs KK)")
    print("="*70)

    player0 = SimpleHand([Card('Ah'), Card('As')])
    player1 = SimpleHand([Card('Kh'), Card('Ks')])

    sim = PokerSimulator(
        players=2,
        community_cards=[],
        player_hands=[player0, player1],
        num_simulations=10000
    )

    print("Running 10,000 simulations...")
    sim.run_simulation()
    sim.print_results()

    print("\nGenerating visualizations...")
    sim.plot_equity_bars()
    sim.plot_outcome_distribution()
    sim.plot_equity_pie_charts()


def demo_three_player_flop():
    """Demo: Three player post-flop visualization"""
    print("\n" + "="*70)
    print("DEMO 2: Three Player Post-Flop")
    print("="*70)

    player0 = SimpleHand([Card('As'), Card('Ks')])  # Top pair
    player1 = SimpleHand([Card('Qh'), Card('Qd')])  # Overpair
    player2 = SimpleHand([Card('Jc'), Card('Tc')])  # Straight draw

    # Flop: K♥Q♠9♦
    community = [Card('Kh'), Card('Qs'), Card('9d')]

    sim = PokerSimulator(
        players=3,
        community_cards=community,
        player_hands=[player0, player1, player2],
        num_simulations=10000
    )

    print("Running 10,000 simulations...")
    sim.run_simulation()
    sim.print_results()

    print("\nGenerating visualizations...")
    sim.plot_equity_bars()
    sim.plot_outcome_distribution()
    sim.plot_equity_pie_charts()


def demo_flush_draw_scenario():
    """Demo: Flush draw vs overpair"""
    print("\n" + "="*70)
    print("DEMO 3: Flush Draw vs Overpair")
    print("="*70)

    player0 = SimpleHand([Card('Ah'), Card('Kh')])  # Flush draw + overcards
    player1 = SimpleHand([Card('Qs'), Card('Qc')])  # Overpair

    # Flop: 9♥7♥2♠
    community = [Card('9h'), Card('7h'), Card('2s')]

    sim = PokerSimulator(
        players=2,
        community_cards=community,
        player_hands=[player0, player1],
        num_simulations=10000
    )

    print("Running 10,000 simulations...")
    sim.run_simulation()
    sim.print_results()

    print("\nGenerating visualizations...")
    sim.plot_equity_bars()
    sim.plot_outcome_distribution()


def demo_equity_convergence():
    """Demo: Equity convergence visualization"""
    print("\n" + "="*70)
    print("DEMO 4: Equity Convergence Over Simulations")
    print("="*70)

    player0 = SimpleHand([Card('Ah'), Card('As')])
    player1 = SimpleHand([Card('Kh'), Card('Ks')])
    player2 = SimpleHand([Card('Qd'), Card('Qc')])

    sim = PokerSimulator(
        players=3,
        community_cards=[],
        player_hands=[player0, player1, player2],
        num_simulations=10000
    )

    print("Running simulation with convergence tracking...")
    sim.run_simulation()

    print("\nGenerating convergence plot (this may take a moment)...")
    sim.plot_equity_convergence(sample_interval=200)


def demo_four_player_tournament():
    """Demo: Four player scenario with all visualizations"""
    print("\n" + "="*70)
    print("DEMO 5: Four Player Tournament Style")
    print("="*70)

    player0 = SimpleHand([Card('As'), Card('Ad')])  # Pocket Aces
    player1 = SimpleHand([Card('Kh'), Card('Kd')])  # Pocket Kings
    player2 = SimpleHand([Card('Ah'), Card('Kh')])  # AK suited
    player3 = SimpleHand([Card('9s'), Card('9c')])  # Pocket Nines

    # Flop: A♣7♣2♠
    community = [Card('Ac'), Card('7c'), Card('2s')]

    sim = PokerSimulator(
        players=4,
        community_cards=community,
        player_hands=[player0, player1, player2, player3],
        num_simulations=10000
    )

    print("Running 10,000 simulations...")
    sim.run_simulation()
    sim.print_results()

    print("\nGenerating all visualizations...")
    sim.plot_equity_bars()
    sim.plot_outcome_distribution()
    sim.plot_equity_pie_charts()


def demo_save_all_visualizations():
    """Demo: Save all visualizations to files"""
    print("\n" + "="*70)
    print("DEMO 6: Save All Visualizations to Files")
    print("="*70)

    player0 = SimpleHand([Card('Ah'), Card('Kh')])
    player1 = SimpleHand([Card('Qs'), Card('Qc')])

    community = [Card('9h'), Card('7h'), Card('2s')]

    sim = PokerSimulator(
        players=2,
        community_cards=community,
        player_hands=[player0, player1],
        num_simulations=10000
    )

    print("Running 10,000 simulations...")
    sim.run_simulation()

    # Create output directory
    output_dir = "visualization_output"

    print(f"\nGenerating and saving all visualizations to '{output_dir}/'...")
    sim.plot_all_visualizations(save_dir=output_dir, show=False)

    print(f"\nVisualizations saved successfully!")
    print(f"Check the '{output_dir}' folder for PNG files.")


def run_all_demos():
    """Run all demonstration scenarios"""
    print("\n" + "="*70)
    print("POKER SIMULATOR VISUALIZATION DEMOS")
    print("="*70)
    print("\nClose each plot window to proceed to the next demo.")
    print("Press Ctrl+C to exit early.\n")

    try:
        demo_two_player_preflop()
        demo_three_player_flop()
        demo_flush_draw_scenario()
        demo_equity_convergence()
        demo_four_player_tournament()
        demo_save_all_visualizations()

        print("\n" + "="*70)
        print("ALL DEMOS COMPLETED!")
        print("="*70)

    except KeyboardInterrupt:
        print("\n\nDemos interrupted by user.")


if __name__ == "__main__":
    # You can run all demos or individual ones
    run_all_demos()

    # Or run specific demos:
    # demo_two_player_preflop()
    # demo_equity_convergence()
    # demo_save_all_visualizations()
