from phevaluator import evaluate_7cards, HandType

def evaluate_hand(cards):
    """
    Evaluates a 7-card poker hand using phevaluator.

    Args:
        cards (list[str]): 7 card strings, e.g. ['Ah', 'Kd', 'Qs', 'Jc', '9h', '2d', '7s']
    Returns:
        int: hand rank (lower = stronger)
    """
    if len(cards) != 7:
        raise ValueError(f"evaluate_hand expects 7 cards, got {len(cards)}")

    rank = evaluate_7cards(*cards)
    hand_type = HandType.name_from_rank(rank)

    # unpack the list into positional arguments
    return rank, hand_type
