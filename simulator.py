import random
from typing import List, Dict, Union, Any
from card import Card
from deck import Deck
from phevaluator import evaluate_cards


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
