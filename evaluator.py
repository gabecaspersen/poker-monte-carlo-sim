from phevaluator import evaluate_cards, evaluate_5cards, evaluate_6cards, evaluate_7cards, HandType


def evaluate_hand(cards):
    """
    Evaluates a poker hand using phevaluator.
    Supports 5, 6, or 7 card hands.

    Args:
        cards (list[str]): Card strings, e.g. ['Ah', 'Kd', 'Qs', 'Jc', '9h', '2d', '7s']

    Returns:
        tuple: (rank: int, hand_type: str)
            - rank: hand rank (lower = stronger, 1 is best)
            - hand_type: string description (e.g., "Straight Flush")

    Raises:
        ValueError: If number of cards is not 5, 6, or 7
    """
    num_cards = len(cards)

    if num_cards == 5:
        rank = evaluate_5cards(*cards)
    elif num_cards == 6:
        rank = evaluate_6cards(*cards)
    elif num_cards == 7:
        rank = evaluate_7cards(*cards)
    else:
        raise ValueError(f"evaluate_hand expects 5, 6, or 7 cards, got {num_cards}")

    hand_type = HandType.name_from_rank(rank)
    return rank, hand_type


def compare_hands(cards1, cards2):
    """
    Compares two poker hands.

    Args:
        cards1 (list[str]): First hand (5, 6, or 7 cards)
        cards2 (list[str]): Second hand (5, 6, or 7 cards)

    Returns:
        int: 1 if cards1 wins, -1 if cards2 wins, 0 if tie
    """
    rank1, _ = evaluate_hand(cards1)
    rank2, _ = evaluate_hand(cards2)

    if rank1 < rank2:  # Lower rank = better hand
        return 1
    elif rank1 > rank2:
        return -1
    else:
        return 0


def get_hand_strength(rank):
    """
    Converts a hand rank to a normalized strength value.

    Args:
        rank (int): Hand rank from phevaluator (1-7462 for 7-card hands)

    Returns:
        float: Hand strength between 0 (worst) and 1 (best)
    """
    # 7462 is the worst possible 7-card hand rank
    max_rank = 7462
    return 1 - (rank - 1) / max_rank


def get_hand_category(hand_type_str):
    """
    Categorizes hand types into broader categories.

    Args:
        hand_type_str (str): Hand type string from phevaluator

    Returns:
        str: Broad category ("premium", "strong", "medium", "weak")
    """
    premium = ["Straight Flush", "Four of a Kind", "Full House"]
    strong = ["Flush", "Straight"]
    medium = ["Three of a Kind", "Two Pair"]

    if hand_type_str in premium:
        return "premium"
    elif hand_type_str in strong:
        return "strong"
    elif hand_type_str in medium:
        return "medium"
    else:
        return "weak"


def calculate_win_rate(wins, losses, ties):
    """
    Calculates win rate and equity from simulation results.

    Args:
        wins (int): Number of wins
        losses (int): Number of losses
        ties (int): Number of ties

    Returns:
        dict: {
            'win_rate': float (0-1),
            'tie_rate': float (0-1),
            'loss_rate': float (0-1),
            'equity': float (0-1),
            'total_simulations': int
        }
    """
    total = wins + losses + ties

    if total == 0:
        return {
            'win_rate': 0.0,
            'tie_rate': 0.0,
            'loss_rate': 0.0,
            'equity': 0.0,
            'total_simulations': 0
        }

    win_rate = wins / total
    tie_rate = ties / total
    loss_rate = losses / total
    equity = win_rate + (tie_rate / 2)  # Equity = wins + half of ties

    return {
        'win_rate': win_rate,
        'tie_rate': tie_rate,
        'loss_rate': loss_rate,
        'equity': equity,
        'total_simulations': total
    }


def rank_to_percentile(rank):
    """
    Converts hand rank to percentile (better than X% of hands).

    Args:
        rank (int): Hand rank from phevaluator

    Returns:
        float: Percentile (0-100), e.g., 95.5 means better than 95.5% of hands
    """
    max_rank = 7462
    percentile = ((max_rank - rank) / max_rank) * 100
    return round(percentile, 2)


class HandEvaluator:
    """
    A class for evaluating and comparing poker hands.
    Provides utilities for Monte Carlo simulation.
    """

    @staticmethod
    def evaluate(cards):
        """Evaluate a poker hand."""
        return evaluate_hand(cards)

    @staticmethod
    def compare(cards1, cards2):
        """Compare two poker hands."""
        return compare_hands(cards1, cards2)

    @staticmethod
    def strength(rank):
        """Get normalized hand strength."""
        return get_hand_strength(rank)

    @staticmethod
    def category(hand_type_str):
        """Get hand category."""
        return get_hand_category(hand_type_str)

    @staticmethod
    def percentile(rank):
        """Convert rank to percentile."""
        return rank_to_percentile(rank)

    @staticmethod
    def win_rate(wins, losses, ties):
        """Calculate win rate statistics."""
        return calculate_win_rate(wins, losses, ties)
