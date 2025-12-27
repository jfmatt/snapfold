#!/usr/bin/env python3
"""
Simple demonstration of exclusive vs inclusive counting.

Shows how to use the exclusive parameter to get different counting modes.
"""

from flexible_poker_analysis_fixed import DeckAnalyzer


def main():
    # Create analyzer for standard 5-card poker
    analyzer = DeckAnalyzer(num_ranks=13, num_suits=4, num_copies=1, hand_size=5)

    print("=" * 70)
    print("DEMONSTRATION: Exclusive vs Inclusive Counting")
    print("=" * 70)

    print("\nStandard 52-card deck, 5-card hands\n")

    # Example 1: Straights
    print("STRAIGHTS:")
    inclusive_straights = analyzer.count_straights(exclusive=False)
    exclusive_straights = analyzer.count_straights(exclusive=True)
    straight_flushes = analyzer.count_straight_flushes()

    print(f"  Inclusive (at least a straight):      {inclusive_straights:>8,}")
    print(f"  Exclusive (straight but not SF):      {exclusive_straights:>8,}")
    print(f"  Difference (straight flushes):        {straight_flushes:>8,}")
    print(f"  Verification: {inclusive_straights} - {straight_flushes} = {exclusive_straights}")

    # Example 2: Three of a kind
    print("\nTHREE OF A KIND:")
    inclusive_3oak = analyzer.count_three_of_kind(exclusive=False)
    exclusive_3oak = analyzer.count_three_of_kind(exclusive=True)
    four_oak = analyzer.count_four_of_kind()
    full_house = analyzer.count_full_house()

    print(f"  Inclusive (at least 3oak):            {inclusive_3oak:>8,}")
    print(f"  Exclusive (3oak only):                {exclusive_3oak:>8,}")
    print(f"  Overlaps with 4oak:                   {four_oak:>8,}")
    print(f"  Overlaps with full house:             {full_house:>8,}")
    print(f"  Note: Exclusive excludes both 4oak and full house")

    # Example 3: Pairs
    print("\nPAIRS:")
    inclusive_pairs = analyzer.count_pairs(exclusive=False)
    exclusive_pairs = analyzer.count_pairs(exclusive=True)
    two_pair = analyzer.count_two_pair()
    three_oak = analyzer.count_three_of_kind()

    print(f"  Inclusive (at least one pair):        {inclusive_pairs:>8,}")
    print(f"  Exclusive (exactly one pair):         {exclusive_pairs:>8,}")
    print(f"  Much lower! Excludes 2-pair, 3oak, etc.")

    # Example 4: Understanding overlaps in 7-card poker
    print("\n" + "=" * 70)
    print("7-CARD POKER (Texas Hold'em)")
    print("=" * 70)

    analyzer7 = DeckAnalyzer(num_ranks=13, num_suits=4, num_copies=1, hand_size=7)

    print("\nWith 7 cards, overlaps become more significant:\n")

    # Three of a kind in 7-card
    inclusive_3oak_7 = analyzer7.count_three_of_kind(exclusive=False)
    exclusive_3oak_7 = analyzer7.count_three_of_kind(exclusive=True)

    print("THREE OF A KIND:")
    print(f"  Inclusive:  {inclusive_3oak_7:>12,} hands ({100*inclusive_3oak_7/analyzer7.count_total_hands():.2f}%)")
    print(f"  Exclusive:  {exclusive_3oak_7:>12,} hands ({100*exclusive_3oak_7/analyzer7.count_total_hands():.2f}%)")
    print(f"  Difference: {inclusive_3oak_7 - exclusive_3oak_7:>12,} hands are also 4oak or full house")

    # Straights and flushes
    straights_7 = analyzer7.count_straights(exclusive=False)
    flushes_7 = analyzer7.count_flushes(exclusive=False)
    sf_7 = analyzer7.count_straight_flushes()

    print("\nSTRAIGHTS AND FLUSHES:")
    print(f"  Straights (inclusive):                {straights_7:>12,}")
    print(f"  Flushes (inclusive):                  {flushes_7:>12,}")
    print(f"  Straight flushes:                     {sf_7:>12,}")
    print(f"  Hands with BOTH straight and flush:   {sf_7:>12,}")
    print(f"  Note: In 7-card, you can have both by using different cards")
    print(f"        E.g., use 5 cards for straight, different 5 for flush")

    print("\n" + "=" * 70)
    print("USE CASES")
    print("=" * 70)
    print("""
Inclusive counting (exclusive=False):
  - Answer: "What are the odds of getting AT LEAST a pair?"
  - Answer: "What are the odds of making AT LEAST a flush?"
  - Useful for: Understanding minimum hand strength probabilities

Exclusive counting (exclusive=True):
  - Answer: "What are the odds of getting EXACTLY a pair (no better)?"
  - Answer: "What are the odds of a flush that isn't a straight flush?"
  - Useful for: Understanding hand distribution without overlaps
  - Note: Categories can still overlap (flush + pair counted in both)
""")


if __name__ == "__main__":
    main()
