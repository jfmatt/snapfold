#!/usr/bin/env python3
"""Test script to demonstrate exclusive vs inclusive counting."""

from flexible_poker_analysis_fixed import DeckAnalyzer


def test_exclusive_vs_inclusive():
    """Compare exclusive and inclusive counts for standard 5-card poker."""

    print("=" * 80)
    print("EXCLUSIVE vs INCLUSIVE COUNTING - Standard 52-card deck, 5 cards")
    print("=" * 80)

    analyzer = DeckAnalyzer(num_ranks=13, num_suits=4, num_copies=1, hand_size=5)
    total_hands = analyzer.count_total_hands()

    print(f"\nTotal possible hands: {total_hands:,}\n")

    # Test each hand type
    hand_types = [
        ("5 of a kind", "count_five_of_kind"),
        ("Straight flush", "count_straight_flushes"),
        ("4 of a kind", "count_four_of_kind"),
        ("Full house", "count_full_house"),
        ("Flush", "count_flushes"),
        ("Straight", "count_straights"),
        ("3 of a kind", "count_three_of_kind"),
        ("Two pair", "count_two_pair"),
        ("Pair", "count_pairs"),
    ]

    print(f"{'Hand Type':<20} {'Inclusive':<15} {'Exclusive':<15} {'Difference':<15}")
    print("-" * 80)

    for hand_name, method_name in hand_types:
        method = getattr(analyzer, method_name)
        inclusive = method(exclusive=False)
        exclusive = method(exclusive=True)
        diff = inclusive - exclusive

        print(f"{hand_name:<20} {inclusive:>14,} {exclusive:>14,} {diff:>14,}")

    # Note: Exclusive counts can overlap!
    print("\n" + "=" * 80)
    print("IMPORTANT: Exclusive counts can still overlap")
    print("=" * 80)
    print("\nBecause hand types like 'flush' and 'pair' are orthogonal (neither contains")
    print("the other), a hand can be counted in multiple exclusive categories.")
    print("\nExample: A flush with a pair is counted as both:")
    print("  - Exclusive flush (flush but not SF)")
    print("  - Exclusive pair (pair but not 2-pair or 3oak)")
    print("\nThis is correct according to the definitional containment rules.")

    # Show traditional poker ranking using mutual exclusion
    print("\n" + "=" * 80)
    print("TRADITIONAL POKER RANKING (mutually exclusive categories)")
    print("=" * 80)
    print("\nFor traditional poker ranking, we need a different approach that considers")
    print("the BEST hand a player can make. This is not the same as exclusive counting!")
    print(f"\n{'Rank':<5} {'Hand Type':<20} {'Count (excl)':<15} {'Probability':<12} {'Odds':<20}")
    print("-" * 80)

    # Calculate mutually exclusive traditional rankings
    # In 5-card poker, straights can't overlap with pairs/trips since a straight
    # requires exactly one card of each rank
    no_pair = total_hands - analyzer.count_pairs(exclusive=False)

    # For traditional ranking, a hand counts in its BEST category only
    # Priority: SF > 4oak > FH > Flush > Straight > 3oak > 2pair > 1pair > high card
    exclusive_hands = [
        ("SF", "Straight flush", analyzer.count_straight_flushes(exclusive=True)),
        ("4oak", "4 of a kind", analyzer.count_four_of_kind(exclusive=True)),
        ("FH", "Full house", analyzer.count_full_house(exclusive=True)),
        ("Fl", "Flush (excl)", analyzer.count_flushes(exclusive=True)),
        ("St", "Straight (excl)", analyzer.count_straights(exclusive=True)),
        ("3oak", "3 of a kind (excl)", analyzer.count_three_of_kind(exclusive=True)),
        ("2P", "Two pair (excl)", analyzer.count_two_pair(exclusive=True)),
        ("1P", "Pair (excl)", analyzer.count_pairs(exclusive=True)),
        ("HC", "High card", no_pair),
    ]

    total_shown = 0
    for rank, hand_name, count in exclusive_hands:
        if count > 0:
            prob = count / total_hands
            odds = f"1 in {total_hands/count:,.1f}" if count > 0 else "N/A"
            print(f"{rank:<5} {hand_name:<20} {count:>14,} {prob:>11.4%} {odds:>20}")
            total_shown += count

    print("-" * 80)
    print(f"{'Total':<26} {total_shown:>14,} {total_shown/total_hands:>11.4%}")
    print(f"\nNote: Total doesn't match because flushes/straights can overlap with rank patterns.")


def test_pinochle_deck():
    """Test exclusive counting on Pinochle deck where 5oak is possible."""

    print("\n\n" + "=" * 80)
    print("EXCLUSIVE vs INCLUSIVE COUNTING - Pinochle deck (48 cards), 5 cards")
    print("=" * 80)

    analyzer = DeckAnalyzer(num_ranks=6, num_suits=4, num_copies=2, hand_size=5)
    total_hands = analyzer.count_total_hands()

    print(f"\nTotal possible hands: {total_hands:,}\n")

    hand_types = [
        ("5 of a kind", "count_five_of_kind"),
        ("Straight flush", "count_straight_flushes"),
        ("4 of a kind", "count_four_of_kind"),
        ("Full house", "count_full_house"),
        ("Flush", "count_flushes"),
        ("Straight", "count_straights"),
        ("3 of a kind", "count_three_of_kind"),
        ("Two pair", "count_two_pair"),
        ("Pair", "count_pairs"),
    ]

    print(f"{'Hand Type':<20} {'Inclusive':<15} {'Exclusive':<15} {'Difference':<15}")
    print("-" * 80)

    for hand_name, method_name in hand_types:
        method = getattr(analyzer, method_name)
        inclusive = method(exclusive=False)
        exclusive = method(exclusive=True)
        diff = inclusive - exclusive

        print(f"{hand_name:<20} {inclusive:>14,} {exclusive:>14,} {diff:>14,}")

    print("\nNote: In Pinochle deck, 5oak is possible due to duplicate cards!")
    print("      4oak exclusive count excludes hands that also have 5oak.")


def test_7_card_hands():
    """Test exclusive counting on 7-card hands (Texas Hold'em style)."""

    print("\n\n" + "=" * 80)
    print("EXCLUSIVE vs INCLUSIVE COUNTING - Standard deck, 7 cards (Hold'em)")
    print("=" * 80)

    analyzer = DeckAnalyzer(num_ranks=13, num_suits=4, num_copies=1, hand_size=7)
    total_hands = analyzer.count_total_hands()

    print(f"\nTotal possible hands: {total_hands:,}\n")

    hand_types = [
        ("5 of a kind", "count_five_of_kind"),
        ("Straight flush", "count_straight_flushes"),
        ("4 of a kind", "count_four_of_kind"),
        ("Full house", "count_full_house"),
        ("Flush", "count_flushes"),
        ("Straight", "count_straights"),
        ("3 of a kind", "count_three_of_kind"),
        ("Two pair", "count_two_pair"),
        ("Pair", "count_pairs"),
    ]

    print(f"{'Hand Type':<20} {'Inclusive':<15} {'Exclusive':<15} {'Difference':<15}")
    print("-" * 80)

    for hand_name, method_name in hand_types:
        method = getattr(analyzer, method_name)
        inclusive = method(exclusive=False)
        exclusive = method(exclusive=True)
        diff = inclusive - exclusive

        print(f"{hand_name:<20} {inclusive:>14,} {exclusive:>14,} {diff:>14,}")

    print("\n" + "=" * 80)
    print("KEY INSIGHT: Notice how inclusive counts overlap significantly")
    print("=" * 80)
    print("\nWith 7 cards:")
    print("  - Many hands have both a straight AND a flush (but not necessarily SF)")
    print("  - Hands with 4oak often also contain a full house (e.g., [4,3] partition)")
    print("  - Almost all hands have at least a pair (79.5% in 7-card)")
    print("\nExclusive counting gives traditional poker hand rankings.")
    print("Inclusive counting shows 'at least' probabilities (useful for analysis).")


if __name__ == "__main__":
    test_exclusive_vs_inclusive()
    test_pinochle_deck()
    test_7_card_hands()
