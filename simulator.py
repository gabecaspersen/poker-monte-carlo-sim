import random
from typing import List, Dict, Union, Any, Optional
from card import Card
from deck import Deck
from phevaluator import evaluate_cards
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


class PokerSimulator:
    """
    Monte Carlo simulator for estimating poker hand probabilities.

    Simulates random deal outcomes to calculate equity for each player.
    """

    def __init__(
        self,
        players: int,
        community_cards: List[Union[Card, str]] = None,
        player_hands: List[Any] = None,
        num_simulations: int = 10000
    ):
        """
        Initialize the poker simulator.

        Args:
            players: Number of players in the hand
            community_cards: List of Card objects or strings (0-5 cards)
            player_hands: List of Hand objects (or any object with hole_cards attribute)
            num_simulations: Number of Monte Carlo iterations to run

        Raises:
            ValueError: If invalid number of players or community cards
        """
        if players < 2:
            raise ValueError("Must have at least 2 players")
        if players > 10:
            raise ValueError("Cannot have more than 10 players")

        self.players = players
        self.num_simulations = num_simulations

        # Convert community cards to Card objects if strings
        if community_cards is None:
            self.community_cards = []
        else:
            self.community_cards = [
                Card(c) if isinstance(c, str) else c
                for c in community_cards
            ]

        if len(self.community_cards) > 5:
            raise ValueError("Cannot have more than 5 community cards")

        # Validate and store player hands
        if player_hands is None:
            self.player_hands = []
        else:
            if len(player_hands) != players:
                raise ValueError(f"Expected {players} hands, got {len(player_hands)}")
            self.player_hands = player_hands

        # Initialize results tracking
        self._results = {
            i: {'wins': 0, 'ties': 0, 'losses': 0}
            for i in range(players)
        }

    def run_simulation(self) -> None:
        """
        Run Monte Carlo simulation to estimate outcomes.

        For each iteration:
        1. Create a fresh deck with known cards removed
        2. Deal remaining community cards
        3. Evaluate all hands
        4. Track wins/ties/losses
        """
        # Reset results
        self._results = {
            i: {'wins': 0, 'ties': 0, 'losses': 0}
            for i in range(self.players)
        }

        for _ in range(self.num_simulations):
            self._simulate_single_hand()

    def _simulate_single_hand(self) -> None:
        """Simulate a single hand outcome."""
        # Create new deck and remove known cards
        deck = Deck()
        known_cards = self.community_cards.copy()

        # Add all hole cards to known cards
        for hand in self.player_hands:
            known_cards.extend(hand.hole_cards)

        deck.remove_cards(known_cards)
        deck.shuffle()

        # Deal remaining community cards
        num_community_needed = 5 - len(self.community_cards)
        simulated_board = self.community_cards.copy()

        if num_community_needed > 0:
            additional_cards = deck.deal(num_community_needed)
            if not isinstance(additional_cards, list):
                additional_cards = [additional_cards]
            simulated_board.extend(additional_cards)

        # Convert board to string format for evaluation
        board_strings = [card.to_string() for card in simulated_board]

        # Evaluate all hands
        hand_ranks = []
        for i, hand in enumerate(self.player_hands):
            hole_strings = [card.to_string() for card in hand.hole_cards]
            all_cards = hole_strings + board_strings
            rank = evaluate_cards(*all_cards)
            hand_ranks.append((i, rank))

        # Find winner(s) - lower rank is better
        best_rank = min(rank for _, rank in hand_ranks)
        winners = [player_id for player_id, rank in hand_ranks if rank == best_rank]

        # Update results
        if len(winners) == 1:
            # Single winner
            winner_id = winners[0]
            self._results[winner_id]['wins'] += 1
            for player_id in range(self.players):
                if player_id != winner_id:
                    self._results[player_id]['losses'] += 1
        else:
            # Tie between multiple players
            for player_id in range(self.players):
                if player_id in winners:
                    self._results[player_id]['ties'] += 1
                else:
                    self._results[player_id]['losses'] += 1

    def calculate_equity(self) -> Dict[int, Dict[str, float]]:
        """
        Calculate equity statistics for each player.

        Returns:
            Dict mapping player_id to statistics:
            {
                player_id: {
                    'win_rate': float (0-1),
                    'tie_rate': float (0-1),
                    'loss_rate': float (0-1),
                    'equity': float (0-1),
                    'wins': int,
                    'ties': int,
                    'losses': int,
                    'total_simulations': int
                }
            }
        """
        equity_results = {}

        for player_id in range(self.players):
            wins = self._results[player_id]['wins']
            ties = self._results[player_id]['ties']
            losses = self._results[player_id]['losses']
            total = wins + ties + losses

            if total == 0:
                equity_results[player_id] = {
                    'win_rate': 0.0,
                    'tie_rate': 0.0,
                    'loss_rate': 0.0,
                    'equity': 0.0,
                    'wins': 0,
                    'ties': 0,
                    'losses': 0,
                    'total_simulations': 0
                }
            else:
                win_rate = wins / total
                tie_rate = ties / total
                loss_rate = losses / total
                equity = win_rate + (tie_rate / 2)

                equity_results[player_id] = {
                    'win_rate': win_rate,
                    'tie_rate': tie_rate,
                    'loss_rate': loss_rate,
                    'equity': equity,
                    'wins': wins,
                    'ties': ties,
                    'losses': losses,
                    'total_simulations': total
                }

        return equity_results

    def get_results_dataframe(self):
        """
        Get results as a pandas DataFrame (if pandas is available).

        Returns:
            pd.DataFrame or None if pandas not available
        """
        try:
            import pandas as pd
            equity_data = self.calculate_equity()

            rows = []
            for player_id, stats in equity_data.items():
                row = {
                    'player_id': player_id,
                    'equity': f"{stats['equity']:.2%}",
                    'win_rate': f"{stats['win_rate']:.2%}",
                    'tie_rate': f"{stats['tie_rate']:.2%}",
                    'loss_rate': f"{stats['loss_rate']:.2%}",
                    'wins': stats['wins'],
                    'ties': stats['ties'],
                    'losses': stats['losses']
                }
                rows.append(row)

            return pd.DataFrame(rows)
        except ImportError:
            return None

    def plot_equity_bars(self, save_path: Optional[str] = None, show: bool = True) -> None:
        """
        Create a bar chart showing equity for each player.

        Args:
            save_path: Optional path to save the figure
            show: Whether to display the plot (default: True)
        """
        equity_data = self.calculate_equity()

        players = list(range(self.players))
        equities = [equity_data[p]['equity'] * 100 for p in players]

        # Create player labels with hole cards
        labels = []
        for p in players:
            hole_cards = [card.to_string() for card in self.player_hands[p].hole_cards]
            labels.append(f"P{p}\n{hole_cards[0]}{hole_cards[1]}")

        # Create color gradient
        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, self.players))

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(labels, equities, color=colors, edgecolor='black', linewidth=1.5)

        # Add value labels on bars
        for bar, equity in zip(bars, equities):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{equity:.1f}%',
                   ha='center', va='bottom', fontweight='bold', fontsize=11)

        ax.set_ylabel('Equity (%)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Player (Hole Cards)', fontsize=12, fontweight='bold')
        ax.set_title(f'Player Equity Distribution\n({self.num_simulations:,} simulations)',
                    fontsize=14, fontweight='bold')
        ax.set_ylim(0, 110)
        ax.grid(axis='y', alpha=0.3, linestyle='--')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
        else:
            plt.close()

    def plot_outcome_distribution(self, save_path: Optional[str] = None, show: bool = True) -> None:
        """
        Create stacked bar chart showing win/tie/loss distribution for each player.

        Args:
            save_path: Optional path to save the figure
            show: Whether to display the plot (default: True)
        """
        equity_data = self.calculate_equity()

        players = list(range(self.players))
        labels = []
        for p in players:
            hole_cards = [card.to_string() for card in self.player_hands[p].hole_cards]
            labels.append(f"P{p}\n{hole_cards[0]}{hole_cards[1]}")

        wins = [equity_data[p]['win_rate'] * 100 for p in players]
        ties = [equity_data[p]['tie_rate'] * 100 for p in players]
        losses = [equity_data[p]['loss_rate'] * 100 for p in players]

        fig, ax = plt.subplots(figsize=(10, 6))

        # Create stacked bars
        ax.bar(labels, wins, label='Wins', color='#2ecc71', edgecolor='black', linewidth=1)
        ax.bar(labels, ties, bottom=wins, label='Ties', color='#f39c12', edgecolor='black', linewidth=1)
        ax.bar(labels, losses, bottom=np.array(wins) + np.array(ties),
               label='Losses', color='#e74c3c', edgecolor='black', linewidth=1)

        ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Player (Hole Cards)', fontsize=12, fontweight='bold')
        ax.set_title(f'Outcome Distribution by Player\n({self.num_simulations:,} simulations)',
                    fontsize=14, fontweight='bold')
        ax.set_ylim(0, 100)
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(axis='y', alpha=0.3, linestyle='--')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
        else:
            plt.close()

    def plot_equity_pie_charts(self, save_path: Optional[str] = None, show: bool = True) -> None:
        """
        Create pie charts showing win/tie/loss breakdown for each player.

        Args:
            save_path: Optional path to save the figure
            show: Whether to display the plot (default: True)
        """
        equity_data = self.calculate_equity()

        # Determine grid layout
        cols = min(3, self.players)
        rows = (self.players + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows))
        if self.players == 1:
            axes = np.array([axes])
        axes = axes.flatten()

        colors = ['#2ecc71', '#f39c12', '#e74c3c']

        for p in range(self.players):
            stats = equity_data[p]
            hole_cards = [card.to_string() for card in self.player_hands[p].hole_cards]

            sizes = [stats['win_rate'] * 100, stats['tie_rate'] * 100, stats['loss_rate'] * 100]
            labels = [f"Win\n{sizes[0]:.1f}%", f"Tie\n{sizes[1]:.1f}%", f"Loss\n{sizes[2]:.1f}%"]

            # Only show non-zero slices
            non_zero_sizes = [s for s in sizes if s > 0]
            non_zero_labels = [l for s, l in zip(sizes, labels) if s > 0]
            non_zero_colors = [c for s, c in zip(sizes, colors) if s > 0]

            axes[p].pie(non_zero_sizes, labels=non_zero_labels, colors=non_zero_colors,
                       autopct='', startangle=90, wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
            axes[p].set_title(f"Player {p}: {hole_cards[0]}{hole_cards[1]}\nEquity: {stats['equity']:.1%}",
                            fontweight='bold', fontsize=11)

        # Hide unused subplots
        for p in range(self.players, len(axes)):
            axes[p].axis('off')

        fig.suptitle(f'Individual Player Outcomes\n({self.num_simulations:,} simulations)',
                    fontsize=14, fontweight='bold')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
        else:
            plt.close()

    def plot_equity_convergence(self, sample_interval: int = 100,
                                save_path: Optional[str] = None, show: bool = True) -> None:
        """
        Plot how equity estimates converge as more simulations run.

        This requires re-running the simulation with tracking.

        Args:
            sample_interval: How often to sample equity (every N simulations)
            save_path: Optional path to save the figure
            show: Whether to display the plot (default: True)
        """
        # Store original results
        original_results = self._results.copy()

        # Track equity over time
        equity_history = {p: [] for p in range(self.players)}
        sample_points = []

        # Reset results
        self._results = {
            i: {'wins': 0, 'ties': 0, 'losses': 0}
            for i in range(self.players)
        }

        # Run simulation with periodic sampling
        for sim in range(1, self.num_simulations + 1):
            self._simulate_single_hand()

            if sim % sample_interval == 0 or sim == self.num_simulations:
                sample_points.append(sim)
                current_equity = self.calculate_equity()
                for p in range(self.players):
                    equity_history[p].append(current_equity[p]['equity'] * 100)

        # Create plot
        fig, ax = plt.subplots(figsize=(12, 6))

        colors = plt.cm.tab10(np.linspace(0, 1, self.players))

        for p in range(self.players):
            hole_cards = [card.to_string() for card in self.player_hands[p].hole_cards]
            label = f"Player {p} ({hole_cards[0]}{hole_cards[1]})"
            ax.plot(sample_points, equity_history[p], label=label,
                   color=colors[p], linewidth=2, marker='o', markersize=3)

        ax.set_xlabel('Number of Simulations', fontsize=12, fontweight='bold')
        ax.set_ylabel('Equity (%)', fontsize=12, fontweight='bold')
        ax.set_title('Equity Convergence Over Simulations', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_ylim(0, 100)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
        else:
            plt.close()

    def plot_all_visualizations(self, save_dir: Optional[str] = None, show: bool = True) -> None:
        """
        Generate all visualization plots.

        Args:
            save_dir: Optional directory to save all figures
            show: Whether to display the plots (default: True)
        """
        import os

        save_paths = {
            'equity_bars': None,
            'outcome_dist': None,
            'pie_charts': None,
            'convergence': None
        }

        if save_dir:
            os.makedirs(save_dir, exist_ok=True)
            save_paths['equity_bars'] = os.path.join(save_dir, 'equity_bars.png')
            save_paths['outcome_dist'] = os.path.join(save_dir, 'outcome_distribution.png')
            save_paths['pie_charts'] = os.path.join(save_dir, 'pie_charts.png')
            save_paths['convergence'] = os.path.join(save_dir, 'equity_convergence.png')

        print("Generating visualizations...")
        print("1/4: Equity bar chart...")
        self.plot_equity_bars(save_path=save_paths['equity_bars'], show=show)

        print("2/4: Outcome distribution...")
        self.plot_outcome_distribution(save_path=save_paths['outcome_dist'], show=show)

        print("3/4: Individual pie charts...")
        self.plot_equity_pie_charts(save_path=save_paths['pie_charts'], show=show)

        print("4/4: Equity convergence...")
        self.plot_equity_convergence(save_path=save_paths['convergence'], show=show)

        print("All visualizations complete!")
        if save_dir:
            print(f"Saved to: {save_dir}")

    def print_results(self) -> None:
        """Print formatted results to console."""
        equity_data = self.calculate_equity()

        print(f"\n{'='*60}")
        print(f"Monte Carlo Simulation Results ({self.num_simulations:,} iterations)")
        print(f"{'='*60}")
        print(f"Community Cards: {[card.to_string() for card in self.community_cards]}")
        print(f"{'='*60}\n")

        for player_id in range(self.players):
            stats = equity_data[player_id]
            hand = self.player_hands[player_id]
            hole_cards = [card.to_string() for card in hand.hole_cards]

            print(f"Player {player_id} - Hole Cards: {hole_cards}")
            print(f"  Equity:    {stats['equity']:.2%}")
            print(f"  Win Rate:  {stats['win_rate']:.2%} ({stats['wins']:,} wins)")
            print(f"  Tie Rate:  {stats['tie_rate']:.2%} ({stats['ties']:,} ties)")
            print(f"  Loss Rate: {stats['loss_rate']:.2%} ({stats['losses']:,} losses)")
            print()
