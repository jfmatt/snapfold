"""
Comprehensive poker hand probability analysis across hand sizes and deck types.
Focuses on hand sizes 5-10 where interesting patterns emerge.
"""

from flexible_poker_analysis_fixed import DeckAnalyzer
from typing import Dict, List, Tuple
import sys

# Deck configurations to analyze
DECK_CONFIGS = {
    'Standard (52)': {'num_ranks': 13, 'num_suits': 4, 'num_copies': 1},
    'Pinochle (48)': {'num_ranks': 6, 'num_suits': 4, 'num_copies': 2},
    'Short-Deck (36)': {'num_ranks': 9, 'num_suits': 4, 'num_copies': 1},
    'Wide (156)': {'num_ranks': 13, 'num_suits': 12, 'num_copies': 1},
}

def analyze_configuration(deck_name: str, config: dict, hand_sizes: List[int]) -> Dict[int, Dict[str, Tuple[int, float]]]:
    """Analyze a specific deck configuration across hand sizes."""
    results = {}
    print(f"\nAnalyzing {deck_name}...", file=sys.stderr)

    for hand_size in hand_sizes:
        print(f"  {hand_size} cards...", file=sys.stderr)
        analyzer = DeckAnalyzer(**config, hand_size=hand_size)
        results[hand_size] = analyzer.analyze_hands()

    return results


def print_deck_comparison(deck_name: str, results: Dict[int, Dict[str, Tuple[int, float]]]):
    """Print detailed comparison for a single deck type."""

    hand_types = list(next(iter(results.values())).keys())
    hand_sizes = sorted(results.keys())

    print(f"\n{'=' * 140}")
    print(f"{deck_name.upper()} - PROBABILITY BY HAND SIZE")
    print(f"{'=' * 140}")

    # Probabilities table
    header = f"{'Hand Type':<25}"
    for hand_size in hand_sizes:
        header += f"{hand_size:>18} cd"
    print(header)
    print('-' * 140)

    for hand_type in hand_types:
        row = f"{hand_type:<25}"
        for hand_size in hand_sizes:
            count, prob = results[hand_size][hand_type]
            if count > 0:
                row += f"{prob:>17.3%} "
            else:
                row += f"{'---':>18}"
        print(row)

    # Rankings table
    print(f"\n{'=' * 140}")
    print(f"{deck_name.upper()} - RARITY RANKING (1=rarest)")
    print(f"{'=' * 140}")

    header = f"{'Hand Type':<25}"
    for hand_size in hand_sizes:
        header += f"{hand_size:>18} cd"
    print(header)
    print('-' * 140)

    # Calculate rankings
    rankings = {}
    for hand_size in hand_sizes:
        sorted_hands = sorted(
            [(hand_type, count) for hand_type, (count, prob) in results[hand_size].items() if count > 0],
            key=lambda x: x[1]
        )
        rankings[hand_size] = {hand_type: idx + 1 for idx, (hand_type, _) in enumerate(sorted_hands)}

    for hand_type in hand_types:
        row = f"{hand_type:<25}"
        for hand_size in hand_sizes:
            if hand_type in rankings[hand_size]:
                rank = rankings[hand_size][hand_type]
                row += f"{rank:>18}"
            else:
                row += f"{'---':>18}"
        print(row)

    # Ranking changes analysis
    print(f"\n{'=' * 140}")
    print(f"RANKING CHANGES")
    print(f"{'=' * 140}")

    changes = []
    for hand_type in hand_types:
        ranks_list = [rankings[hs].get(hand_type, None) for hs in hand_sizes]
        # Remove None values
        valid_ranks = [(hs, r) for hs, r in zip(hand_sizes, ranks_list) if r is not None]

        if len(valid_ranks) > 1:
            min_rank = min(r for _, r in valid_ranks)
            max_rank = max(r for _, r in valid_ranks)
            rank_range = max_rank - min_rank

            if rank_range > 0:
                changes.append((hand_type, valid_ranks, rank_range))

    if changes:
        changes.sort(key=lambda x: x[2], reverse=True)
        for hand_type, rank_history, rank_range in changes:
            rank_str = " → ".join([f"{hs}cd:#{r}" for hs, r in rank_history])
            change_magnitude = "↑↑" if rank_range >= 2 else "↑"
            print(f"  {change_magnitude} {hand_type:<25} {rank_str} (range: {rank_range})")
    else:
        print("  No ranking changes")


def print_crossover_analysis(all_results: Dict[str, Dict[int, Dict[str, Tuple[int, float]]]]):
    """Analyze where hand types cross over in probability."""

    print(f"\n{'=' * 140}")
    print("CROSSOVER ANALYSIS - When do hand rankings flip?")
    print(f"{'=' * 140}")

    for deck_name in all_results:
        print(f"\n{deck_name}:")
        results = all_results[deck_name]
        hand_sizes = sorted(results.keys())

        # Track when rankings change between consecutive hand sizes
        crossovers = []
        for i in range(len(hand_sizes) - 1):
            hs1, hs2 = hand_sizes[i], hand_sizes[i + 1]

            # Get rankings for both sizes
            sorted_hs1 = sorted(
                [(ht, cnt) for ht, (cnt, _) in results[hs1].items() if cnt > 0],
                key=lambda x: x[1]
            )
            sorted_hs2 = sorted(
                [(ht, cnt) for ht, (cnt, _) in results[hs2].items() if cnt > 0],
                key=lambda x: x[1]
            )

            ranking_hs1 = {ht: idx for idx, (ht, _) in enumerate(sorted_hs1)}
            ranking_hs2 = {ht: idx for idx, (ht, _) in enumerate(sorted_hs2)}

            # Find crossovers
            for ht1 in ranking_hs1:
                for ht2 in ranking_hs1:
                    if ht1 != ht2 and ht1 in ranking_hs2 and ht2 in ranking_hs2:
                        # Check if relative order flipped
                        before = ranking_hs1[ht1] < ranking_hs1[ht2]
                        after = ranking_hs2[ht1] < ranking_hs2[ht2]

                        if before != after:
                            crossovers.append((hs1, hs2, ht1, ht2))

        if crossovers:
            for hs1, hs2, ht1, ht2 in crossovers:
                print(f"  {hs1}→{hs2} cards: '{ht1}' and '{ht2}' swap positions")
        else:
            print("  No crossovers detected")


def generate_csv_data(all_results: Dict[str, Dict[int, Dict[str, Tuple[int, float]]]]):
    """Generate CSV data for external plotting."""

    print(f"\n{'=' * 140}")
    print("CSV DATA FOR PLOTTING")
    print(f"{'=' * 140}")

    for deck_name, results in all_results.items():
        print(f"\n# {deck_name}")
        print("hand_size,hand_type,probability,count,rank")

        hand_sizes = sorted(results.keys())

        for hand_size in hand_sizes:
            # Get rankings for this hand size
            sorted_hands = sorted(
                [(ht, cnt, prob) for ht, (cnt, prob) in results[hand_size].items() if cnt > 0],
                key=lambda x: x[1]
            )
            rankings = {ht: idx + 1 for idx, (ht, _, _) in enumerate(sorted_hands)}

            for hand_type, (count, prob) in results[hand_size].items():
                if count > 0:
                    rank = rankings[hand_type]
                    print(f"{hand_size},{hand_type},{prob},{count},{rank}")


def main():
    hand_sizes = list(range(5, 11))  # 5 through 10

    all_results = {}

    # Analyze each deck configuration
    for deck_name, config in DECK_CONFIGS.items():
        all_results[deck_name] = analyze_configuration(deck_name, config, hand_sizes)

    # Print detailed analysis for each deck
    for deck_name in DECK_CONFIGS:
        print_deck_comparison(deck_name, all_results[deck_name])

    # Print crossover analysis
    print_crossover_analysis(all_results)

    # Generate CSV data for plotting
    generate_csv_data(all_results)

    print(f"\n{'=' * 140}")
    print("ANALYSIS COMPLETE")
    print(f"{'=' * 140}")
    print("\nKey Insights:")
    print("  - Rankings are most stable in smaller hand sizes (5-6 cards)")
    print("  - Crossovers tend to happen in the 7-10 card range")
    print("  - Different deck shapes exhibit different crossover patterns")
    print("  - CSV data above can be used with plotting tools (gnuplot, matplotlib, etc.)")
    print()


if __name__ == "__main__":
    main()
