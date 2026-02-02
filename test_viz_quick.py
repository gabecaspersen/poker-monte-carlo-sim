"""
Quick test to verify visualizations work without showing plots.
"""

from card import Card
from simulator import PokerSimulator


class SimpleHand:
    """Simple hand class for testing."""
    def __init__(self, hole_cards):
        self.hole_cards = hole_cards


def quick_test():
    """Quick test of visualization functionality"""
    print("Testing visualization functionality...")

    player0 = SimpleHand([Card('Ah'), Card('As')])
    player1 = SimpleHand([Card('Kh'), Card('Ks')])

    sim = PokerSimulator(
        players=2,
        community_cards=[],
        player_hands=[player0, player1],
        num_simulations=1000
    )

    print("Running 1,000 simulations...")
    sim.run_simulation()
    sim.print_results()

    print("\nGenerating visualizations (saving to files, not displaying)...")

    # Test each visualization method
    print("- Equity bars...")
    sim.plot_equity_bars(save_path="test_equity_bars.png", show=False)

    print("- Outcome distribution...")
    sim.plot_outcome_distribution(save_path="test_outcome_dist.png", show=False)

    print("- Pie charts...")
    sim.plot_equity_pie_charts(save_path="test_pie_charts.png", show=False)

    print("- Convergence plot...")
    sim.plot_equity_convergence(sample_interval=100, save_path="test_convergence.png", show=False)

    print("\nAll visualizations generated successfully!")
    print("Check for test_*.png files in the current directory.")

if __name__ == "__main__":
    quick_test()
