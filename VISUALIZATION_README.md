# PokerSimulator Visualizations

Comprehensive visualization methods for analyzing Monte Carlo poker simulation results.

## Features

The `PokerSimulator` class includes four main visualization methods:

1. **Equity Bar Charts** - Compare player equities side-by-side
2. **Outcome Distribution** - Stacked bars showing win/tie/loss breakdown
3. **Individual Pie Charts** - Per-player outcome visualization
4. **Equity Convergence** - Track how equity estimates stabilize over simulations

## Installation Requirements

```bash
pip install matplotlib numpy
```

## Visualization Methods

### 1. `plot_equity_bars()`

Creates a bar chart comparing equity across all players.

**Features:**
- Color gradient from red (low equity) to green (high equity)
- Displays hole cards for each player
- Shows equity percentage on top of each bar

**Usage:**
```python
from card import Card
from simulator import PokerSimulator

class SimpleHand:
    def __init__(self, hole_cards):
        self.hole_cards = hole_cards

player0 = SimpleHand([Card('Ah'), Card('As')])
player1 = SimpleHand([Card('Kh'), Card('Ks')])

sim = PokerSimulator(
    players=2,
    community_cards=[],
    player_hands=[player0, player1],
    num_simulations=10000
)

sim.run_simulation()
sim.plot_equity_bars()
```

**Parameters:**
- `save_path` (str, optional): Path to save the figure as PNG
- `show` (bool, default=True): Whether to display the plot

**Example:**
```python
sim.plot_equity_bars(save_path='equity_bars.png', show=True)
```

---

### 2. `plot_outcome_distribution()`

Creates a stacked bar chart showing win/tie/loss percentages for each player.

**Features:**
- Green for wins, orange for ties, red for losses
- 100% stacked format for easy comparison
- Shows exact percentage breakdown

**Usage:**
```python
sim.run_simulation()
sim.plot_outcome_distribution()
```

**Parameters:**
- `save_path` (str, optional): Path to save the figure
- `show` (bool, default=True): Whether to display the plot

---

### 3. `plot_equity_pie_charts()`

Creates individual pie charts for each player showing their win/tie/loss breakdown.

**Features:**
- One pie chart per player
- Displays equity percentage in title
- Automatic grid layout (up to 3 columns)
- Only shows non-zero slices

**Usage:**
```python
sim.run_simulation()
sim.plot_equity_pie_charts()
```

**Parameters:**
- `save_path` (str, optional): Path to save the figure
- `show` (bool, default=True): Whether to display the plot

---

### 4. `plot_equity_convergence()`

Plots how equity estimates converge as more simulations are run.

**Features:**
- Line plot showing equity over time
- Different color for each player
- Useful for determining optimal simulation count
- Re-runs simulation with tracking

**Usage:**
```python
sim.run_simulation()
sim.plot_equity_convergence(sample_interval=100)
```

**Parameters:**
- `sample_interval` (int, default=100): How often to sample equity
- `save_path` (str, optional): Path to save the figure
- `show` (bool, default=True): Whether to display the plot

**Note:** This method re-runs the simulation to track convergence, so it may take longer.

---

### 5. `plot_all_visualizations()`

Convenience method to generate all visualizations at once.

**Usage:**
```python
sim.run_simulation()
sim.plot_all_visualizations(save_dir='output', show=False)
```

**Parameters:**
- `save_dir` (str, optional): Directory to save all figures
- `show` (bool, default=True): Whether to display plots

**Generated files:**
- `equity_bars.png`
- `outcome_distribution.png`
- `pie_charts.png`
- `equity_convergence.png`

## Complete Examples

### Example 1: Two Player Pre-flop Analysis

```python
from card import Card
from simulator import PokerSimulator

class SimpleHand:
    def __init__(self, hole_cards):
        self.hole_cards = hole_cards

# AA vs KK pre-flop
player0 = SimpleHand([Card('Ah'), Card('As')])
player1 = SimpleHand([Card('Kh'), Card('Ks')])

sim = PokerSimulator(
    players=2,
    community_cards=[],
    player_hands=[player0, player1],
    num_simulations=10000
)

sim.run_simulation()

# Generate all visualizations
sim.plot_equity_bars()
sim.plot_outcome_distribution()
sim.plot_equity_pie_charts()
sim.plot_equity_convergence(sample_interval=200)
```

### Example 2: Three Player Post-Flop Analysis

```python
# Top pair vs Overpair vs Straight draw
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

sim.run_simulation()
sim.plot_equity_bars()
sim.plot_outcome_distribution()
sim.plot_equity_pie_charts()
```

### Example 3: Save All Visualizations to Files

```python
player0 = SimpleHand([Card('Ah'), Card('Kh')])  # Flush draw
player1 = SimpleHand([Card('Qs'), Card('Qc')])  # Overpair

community = [Card('9h'), Card('7h'), Card('2s')]

sim = PokerSimulator(
    players=2,
    community_cards=community,
    player_hands=[player0, player1],
    num_simulations=10000
)

sim.run_simulation()

# Save all visualizations without displaying
sim.plot_all_visualizations(save_dir='poker_analysis', show=False)
```

### Example 4: Four Player Tournament

```python
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

sim.run_simulation()
sim.print_results()

# Generate visualizations
sim.plot_equity_bars()
sim.plot_outcome_distribution()
sim.plot_equity_pie_charts()
```

## Testing Visualizations

Run the comprehensive demo:
```bash
python test_visualizations.py
```

This will demonstrate all visualization types with various poker scenarios.

For a quick non-interactive test:
```bash
python test_viz_quick.py
```

This generates all visualizations and saves them as PNG files without displaying.

## Customization Tips

### Adjusting Figure Size

You can modify the figure size by editing the `figsize` parameter in the source:

```python
# In simulator.py, change:
fig, ax = plt.subplots(figsize=(10, 6))
# To:
fig, ax = plt.subplots(figsize=(12, 8))
```

### Changing Colors

Color schemes can be customized in each method:

```python
# Equity bars - uses RdYlGn colormap (Red-Yellow-Green)
colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, self.players))

# Outcome distribution - manual colors
wins: '#2ecc71' (green)
ties: '#f39c12' (orange)
losses: '#e74c3c' (red)
```

### Adjusting Convergence Sampling

For more detailed convergence plots, decrease the sample interval:

```python
# More samples = smoother curve but slower
sim.plot_equity_convergence(sample_interval=50)

# Fewer samples = faster but less smooth
sim.plot_equity_convergence(sample_interval=500)
```

## Performance Considerations

- **Standard plots** (bars, distributions, pie charts): Very fast (~instant)
- **Convergence plots**: Slower as they re-run the simulation with tracking
  - 10,000 simulations with interval=100: ~2-5 seconds
  - 50,000 simulations with interval=500: ~10-15 seconds

## Output Files

When saving visualizations, recommended DPI is 300 for publication quality:

```python
sim.plot_equity_bars(save_path='equity.png')  # Uses default 300 DPI
```

Files are saved as PNG with:
- High resolution (300 DPI)
- Tight bounding box (no extra whitespace)
- Transparent background support

## Interpretation Guide

### Equity Bar Chart
- **Height = Win probability + (Tie probability / 2)**
- Useful for quickly identifying favorites
- Color coding helps spot underdogs vs favorites

### Outcome Distribution
- **100% stacked** shows relative chances
- Large green section = strong favorite
- Significant orange = many split pots (e.g., similar hands)
- Large red = underdog

### Pie Charts
- **Individual perspective** for each player
- Useful for multi-player scenarios
- Equity shown in title for quick reference

### Convergence Plot
- **Flat line = converged** estimate
- **Still trending** = need more simulations
- Different convergence rates show certainty levels
- Tight convergence (< 1000 sims) = very lopsided scenario
- Slow convergence = close race

## Common Use Cases

1. **Hand analysis** - Understand equity in specific situations
2. **Strategy development** - Identify profitable plays
3. **Educational** - Visualize poker concepts
4. **Content creation** - Generate graphics for articles/videos
5. **Tournament analysis** - Multi-player equity distribution

## Files

- **[simulator.py](simulator.py)** - Main PokerSimulator class with visualization methods
- **[test_visualizations.py](test_visualizations.py)** - Comprehensive demo suite
- **[test_viz_quick.py](test_viz_quick.py)** - Quick non-interactive test

## Dependencies

```
matplotlib >= 3.0
numpy >= 1.19
phevaluator
```

## Future Enhancements

Potential additions:
- Heatmaps for range vs range analysis
- 3D plots for three-player scenarios
- Animation showing equity changes across streets
- Probability density functions
- Interactive plots with Plotly
