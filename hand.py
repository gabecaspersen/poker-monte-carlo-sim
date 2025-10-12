from evaluator.evaluator import evaluate_hand


class Hand:
    def __init__(self, hole_cards, player_id=None):
        self.hole_cards = hole_cards
        self.rank = None
        self.type = None
        self.equity = None
        self.best_hand = None
        self.player_id = player_id


    def evaluate(self, board):
        all_cards = self.hole + board
        return evaluate_hand(all_cards)
    
    
    def update_equity(self, equity):
        self.equity = equity
    

    def reset(self): 
        self.rank = None
        self.type = None
        self.equity = None
        self.best_hand = None

    def __lt__(self, other):
        return self.rank > other.rank
    
    def __eq__(self, other):
        return self.rank == other.rank
    
    def __repr__(self):
        return f"Hand({self.hole_cards}, rank={self.rank}, type={self.type}, equity={self.equity})"
    
