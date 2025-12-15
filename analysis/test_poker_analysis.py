#!/usr/bin/env python3
"""Test script to verify poker hand calculations."""

from flexible_poker_analysis_fixed import DeckAnalyzer
from dataclasses import dataclass

@dataclass
class ExpectedCounts:
    total: int
    straight_flushes: int
    four_oaks: int
    full_houses: int
    flushes: int
    straights: int
    three_oaks: int
    two_pairs: int
    pairs: int


def test_deck(analyzer: DeckAnalyzer, expected: ExpectedCounts):
    def expect(actual: int, expected: int):
        print(f"  Expected: {expected:,}")
        print(f"  Actual:   {actual:,}")
        print(f"  Result:   {'✓ PASS' if actual == expected else '✗ FAIL'}")

    print(f"\nStraight Flush:")
    expect(analyzer.count_straight_flushes(), expected.straight_flushes)

    print(f"\n4oak:")
    expect(analyzer.count_four_of_kind(), expected.four_oaks)

    print(f"\nFull House:")
    expect(analyzer.count_full_house(), expected.full_houses)

    print(f"\nFlush:")
    expect(analyzer.count_flushes(), expected.flushes)

    print(f"\nStraight:")
    expect(analyzer.count_straights(), expected.straights)

    print(f"\n3oak:")
    expect(analyzer.count_three_of_kind(), expected.three_oaks)

    print(f"\n2 pair:")
    expect(analyzer.count_two_pair(), expected.two_pairs)

    print(f"\nPair:")
    expect(analyzer.count_pairs(), expected.pairs)

    print(f"\nTotal hands:")
    expect(analyzer.count_total_hands(), expected.total)

def test_standard_7card():
    print("Testing standard 7-card calculations...")

    # Expected values from https://www.durangobill.com/Poker_Probabilities_7_Cards.html
    analyzer = DeckAnalyzer(num_ranks=13, num_suits=4, num_copies=1, hand_size=7)

    # Test straight flush calculation
    sf_count = analyzer.count_straight_flushes()
    expected_sf = 4324 + 37260

    print(f"\nStraight Flush:")
    print(f"  Expected: {expected_sf:,}")
    print(f"  Actual:   {sf_count:,}")
    print(f"  Result:   {'✓ PASS' if sf_count == expected_sf else '✗ FAIL'}")

    # Test total hands
    total = analyzer.count_total_hands()
    expected_total = 133784560  # C(52, 7)

    print(f"\nTotal Hands:")
    print(f"  Expected: {expected_total:,}")
    print(f"  Actual:   {total:,}")
    print(f"  Result:   {'✓ PASS' if total == expected_total else '✗ FAIL'}")

    # test straights
    straights = analyzer.count_straights()
    expected_straights = 747980 + 5432040 + expected_sf
    print(f"\nStraight:")
    print(f"  Expected: {expected_straights:,}")
    print(f"  Actual:   {straights:,}")
    print(f"  Result:   {'✓ PASS' if straights == expected_straights else '✗ FAIL'}")

    # Test flush calculation
    flush_count = analyzer.count_flushes()
    expected_flush_total = 4047644 + expected_sf

    print(f"\nFlush:")
    print(f"  Expected: {expected_flush_total:,}")
    print(f"  Actual:   {flush_count:,}")
    print(f"  Result:   {'✓ PASS' if flush_count == expected_flush_total else '✗ FAIL'}")


def test_short_deck_7card():
    """Test short-deck 7-card calculations against known values."""
    print("Testing Short-Deck 7-card poker calculations...")

    analyzer = DeckAnalyzer(num_ranks=9, num_suits=4, num_copies=1, hand_size=7)

    # Test straight flush calculation
    sf_count = analyzer.count_straight_flushes()
    expected_sf = 10560  # From blog post: 1,860 + 8,700

    print(f"\nStraight Flush:")
    print(f"  Expected: {expected_sf:,}")
    print(f"  Actual:   {sf_count:,}")
    print(f"  Result:   {'✓ PASS' if sf_count == expected_sf else '✗ FAIL'}")

    # Test total hands
    total = analyzer.count_total_hands()
    expected_total = 8347680  # C(36, 7)

    print(f"\nTotal Hands:")
    print(f"  Expected: {expected_total:,}")
    print(f"  Actual:   {total:,}")
    print(f"  Result:   {'✓ PASS' if total == expected_total else '✗ FAIL'}")

    # Test flush calculation
    # Let's manually verify the flush count
    # For 7 cards from 36, getting at least 5 of same suit:
    # Each suit has 9 cards
    # Ways to get exactly 5 from one suit and 2 from others: C(9,5) * C(27,2)
    # Ways to get exactly 6 from one suit and 1 from others: C(9,6) * C(27,1)
    # Ways to get exactly 7 from one suit: C(9,7)

    import math
    C = lambda n, k: math.factorial(n) // (math.factorial(k) * math.factorial(n-k))

    flush_5 = C(9, 5) * C(27, 2)  # 126 * 351 = 44,226
    flush_6 = C(9, 6) * C(27, 1)  # 84 * 27 = 2,268
    flush_7 = C(9, 7)              # 36
    expected_flush_per_suit = flush_5 + flush_6 + flush_7  # 46,530
    expected_flush_total = 4 * expected_flush_per_suit  # 186,120

    flush_count = analyzer.count_flushes()

    print(f"\nFlush:")
    print(f"  Expected: {expected_flush_total:,}")
    print(f"  Actual:   {flush_count:,}")
    print(f"  Result:   {'✓ PASS' if flush_count == expected_flush_total else '✗ FAIL'}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Testing Standard 5-card poker calculations...")
    test_deck(
        DeckAnalyzer(num_ranks=13, num_suits=4, num_copies=1, hand_size=5),
        # Expectations from https://meteor.geol.iastate.edu/~jdduda/portfolio/492.pdf
        ExpectedCounts(
            total= 2598960,
            straight_flushes= 40,
            four_oaks= 624,
            full_houses= 3744,
            flushes= 5108 + 40, # includes straight flush
            straights = 10200 + 40, # includes straight flush
            three_oaks = 54912 + 3744 + 624, # includes full house and 4oak
            two_pairs = 123552 + 3744, # includes full house
            pairs = 1098240 + 123552 + 54912 + 3744 + 624, # includes two pair, 3oak, full house, 4oak
        )
    )

    print("\n" + "="*60)
    print("Testing Standard 7-card poker calculations...")
    test_deck(
        DeckAnalyzer(num_ranks=13, num_suits=4, num_copies=1, hand_size=7),
        # Expectations from https://www.durangobill.com/Poker_Probabilities_7_Cards.html
        ExpectedCounts(
            total = 133784560,
            straight_flushes = 4324 + 37260,
            four_oaks = 224848,
            full_houses = 3473184,
            flushes = 4047644 + 4324 + 37260, # includes straight flush
            straights = 747980 + 5432040 + 4324 + 37260, # includes straight flush
            three_oaks = 6461620 + 3473184 + 224848, # includes full house and 4oak
            two_pairs = 31433400 + 3473184, # includes full house
            pairs = 18188280 + 40439520 + 31433400 + 6461620 + 3473184 + 224848, # includes two pair, 3oak, full house, 4oak
        )
    )

    print("\n" + "="*60)
    print("All tests completed!")
