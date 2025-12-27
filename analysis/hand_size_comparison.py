"""
Compare poker hand probabilities across different hand sizes.
Shows how relative probabilities change as hand size increases.
"""

from flexible_poker_analysis_fixed import DeckAnalyzer
from typing import Dict, List, Tuple
import sys

def analyze_hand_sizes(hand_sizes: List[int]) -> Dict[int, Dict[str, Tuple[int, float]]]:
    """Analyze a standard deck with different hand sizes."""
    results = {}

    for hand_size in hand_sizes:
        print(f"Analyzing {hand_size}-card hands...", file=sys.stderr)
        analyzer = DeckAnalyzer(num_ranks=13, num_suits=4, num_copies=1, hand_size=hand_size)
        results[hand_size] = analyzer.analyze_hands()

    return results

def print_comparison_table(results: Dict[int, Dict[str, Tuple[int, float]]]):
    """Print a comparison table of probabilities across hand sizes."""

    # Get all hand types (from any result set)
    hand_types = list(next(iter(results.values())).keys())
    hand_sizes = sorted(results.keys())

    # Print header
    print("\n" + "=" * 120)
    print("POKER HAND PROBABILITY COMPARISON - STANDARD DECK")
    print("How probabilities change as hand size increases")
    print("=" * 120)

    # Print column headers
    header = f"{'Hand Type':<30}"
    for hand_size in hand_sizes:
        header += f"{hand_size:>20} cards"
    print(header)
    print("-" * 120)

    # Print probabilities for each hand type
    for hand_type in hand_types:
        row = f"{hand_type:<30}"
        for hand_size in hand_sizes:
            count, prob = results[hand_size][hand_type]
            if count > 0:
                row += f"{prob:>19.4%} "
            else:
                row += f"{'---':>20}"
        print(row)

    print("\n" + "=" * 120)
    print("RARITY RANKING (1 = rarest, higher = more common)")
    print("=" * 120)

    # Print ranking header
    header = f"{'Hand Type':<30}"
    for hand_size in hand_sizes:
        header += f"{hand_size:>20} cards"
    print(header)
    print("-" * 120)

    # For each hand size, create a ranking
    rankings = {}
    for hand_size in hand_sizes:
        # Sort by probability (count)
        sorted_hands = sorted(
            [(hand_type, count, prob) for hand_type, (count, prob) in results[hand_size].items() if count > 0],
            key=lambda x: x[1]
        )
        # Create ranking dict
        rankings[hand_size] = {hand_type: idx + 1 for idx, (hand_type, _, _) in enumerate(sorted_hands)}

    # Print rankings for each hand type
    for hand_type in hand_types:
        row = f"{hand_type:<30}"
        for hand_size in hand_sizes:
            if hand_type in rankings[hand_size]:
                rank = rankings[hand_size][hand_type]
                row += f"{rank:>20}"
            else:
                row += f"{'---':>20}"
        print(row)

    print("\n" + "=" * 120)
    print("ODDS (1 in X)")
    print("=" * 120)

    # Print odds header
    header = f"{'Hand Type':<30}"
    for hand_size in hand_sizes:
        header += f"{hand_size:>20} cards"
    print(header)
    print("-" * 120)

    # Get total hands for each size
    total_hands = {}
    for hand_size in hand_sizes:
        analyzer = DeckAnalyzer(num_ranks=13, num_suits=4, num_copies=1, hand_size=hand_size)
        total_hands[hand_size] = analyzer.count_total_hands()

    # Print odds for each hand type
    for hand_type in hand_types:
        row = f"{hand_type:<30}"
        for hand_size in hand_sizes:
            count, prob = results[hand_size][hand_type]
            if count > 0:
                odds = total_hands[hand_size] / count
                if odds >= 1000:
                    row += f"{f'1 in {odds:,.0f}':>20}"
                else:
                    row += f"{f'1 in {odds:.1f}':>20}"
            else:
                row += f"{'---':>20}"
        print(row)

    print("\n" + "=" * 120)
    print("KEY INSIGHTS")
    print("=" * 120)

    # Analyze trends
    print("\nAs hand size increases:")
    print("  - All hand types become MORE common (probabilities increase)")
    print("  - But the RELATIVE rankings can change!")
    print("  - More cards = more opportunities to make each hand type")
    print()


def main():
    hand_sizes = [5, 7, 10, 14]
    results = analyze_hand_sizes(hand_sizes)
    print_comparison_table(results)


if __name__ == "__main__":
    main()
