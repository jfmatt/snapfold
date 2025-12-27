#!/usr/bin/env python3
"""Test script to verify poker hand calculations."""

from flexible_poker_analysis_fixed import DeckAnalyzer
from dataclasses import dataclass

@dataclass
class ExpectedCounts:
    total: int
    straight_flushes: int
    five_oaks: int
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

    print(f"\n5oak:")
    expect(analyzer.count_five_of_kind(), expected.five_oaks)

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
            five_oaks= 0,
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
        # Note: using FULLY inclusive counting based on rank patterns only
        # This counts hands by whether they meet the rank pattern criteria,
        # REGARDLESS of straights/flushes. So a hand that is both a full house
        # AND a straight is counted in both categories.
        ExpectedCounts(
            total = 133784560,
            straight_flushes = 41584,  # Calculated via inclusion-exclusion
            five_oaks = 0,
            four_oaks = 224848,  # Partition-based (matches DurangoBill since 4oak can't be a straight/flush)
            full_houses = 3514992,  # Partition-based (includes full houses that are also straights)
            flushes = 4089228,  # Includes straight flushes
            straights = 6454272,  # Includes straight flushes AND non-SF flushes with straights
            three_oaks = 10287472,  # Partition-based (includes 3oak that are also straights/flushes)
            two_pairs = 35638512,  # Partition-based (includes 2pair that are also straights/flushes)
            pairs = 105669616,  # Partition-based (includes pairs that are also straights/flushes)
        )
    )

    print("\n" + "="*60)
    print("Testing Short Deck (6-plus) 5-card poker calculations...")
    test_deck(
        DeckAnalyzer(num_ranks=9, num_suits=4, num_copies=1, hand_size=5),
        # Short deck poker: ranks 6-7-8-9-10-J-Q-K-A (9 ranks, 36 cards total)
        # Reference from twoplustwo.txt (exclusive counting)
        # For 5-card hands, most values match reference exactly since overlaps are minimal
        ExpectedCounts(
            total = 376992,  # C(36, 5) - matches reference
            straight_flushes = 24,  # Matches reference: 4 (royal) + 20 (other)
            five_oaks = 0,
            four_oaks = 288,  # Matches reference exactly
            full_houses = 1728,  # Matches reference exactly
            flushes = 504,  # Matches reference: 480 + 24 (SF)
            straights = 6144,  # Matches reference: 6,120 + 24 (SF)
            three_oaks = 18144,  # Inclusive: 1,728 (FH) + 288 (4oak) + 16,128 (3oak only)
            two_pairs = 38016,  # Inclusive: 1,728 (FH) + 36,288 (2pair only)
            pairs = 247968,  # Partition-based (all partitions with val >= 2)
        )
    )

    print("\n" + "="*60)
    print("Testing Short Deck (6-plus) 7-card poker calculations...")
    test_deck(
        DeckAnalyzer(num_ranks=9, num_suits=4, num_copies=1, hand_size=7),
        # Short deck poker: ranks 6-7-8-9-10-J-Q-K-A (9 ranks, 36 cards total)
        # Reference: https://forumserver.twoplustwo.com/25/probability/short-deck-six-plus-hold-em-hand-rankings-1685367/
        # Note: Reference uses exclusive counting (traditional poker ranking)
        # We use FULLY inclusive counting based on rank patterns
        ExpectedCounts(
            total = 8347680,  # C(36, 7)
            straight_flushes = 10560,  # Matches reference: 1,860 (royal) + 8,700 (other SF)
            five_oaks = 0,
            four_oaks = 44640,  # Matches reference (4oak can't overlap with straights/flushes)
            full_houses = 645408,  # Partition-based (includes [4,3] and [4,2,1] which have 4oak)
            flushes = 186120,  # Matches reference: 175,560 + 10,560 (SF)
            straights = 1213440,  # Inclusive (includes hands with straights + flushes, straights + 3oak, etc.)
            three_oaks = 1322784,  # Partition-based (includes full houses and 4oak)
            two_pairs = 3983904,  # Partition-based (includes full houses and straights)
            pairs = 7757856,  # Partition-based (includes all hands with any pair)
        )
    )

    print("\n" + "="*60)
    print("Testing Pinochle Deck 5-card poker calculations...")
    test_deck(
        DeckAnalyzer(num_ranks=6, num_suits=4, num_copies=2, hand_size=5),
        # Pinochle deck: ranks 9-10-J-Q-K-A (6 ranks, 48 cards total, 2 copies each)
        # With 8 cards per rank (4 suits × 2 copies), 5oak is possible
        # Calculated using partition-based inclusive counting
        ExpectedCounts(
            total = 1712304,
            straight_flushes = 384,
            five_oaks = 336,  # Possible with 8 cards per rank!
            four_oaks = 17136,
            full_houses = 47040,
            flushes = 3168,
            straights = 98304,
            three_oaks = 279216,
            two_pairs = 423360,
            pairs = 1515696,
        )
    )

    print("\n" + "="*60)
    print("Testing Fantasy 6-Suit Deck 5-card poker calculations...")
    test_deck(
        DeckAnalyzer(num_ranks=13, num_suits=6, num_copies=1, hand_size=5),
        # Fantasy deck: standard ranks (13) but 6 suits instead of 4 (78 cards total)
        # With 6 cards per rank (6 suits × 1 copy), 5oak is possible but very rare
        # Flushes much rarer due to cards spread across more suits
        ExpectedCounts(
            total = 21111090,
            straight_flushes = 60,
            five_oaks = 78,  # Possible with 6 cards per rank, but extremely rare!
            four_oaks = 14118,
            full_houses = 46800,
            flushes = 7722,  # Much rarer than standard deck (0.04% vs 0.20%)
            straights = 77760,
            three_oaks = 678678,
            two_pairs = 1205100,
            pairs = 11103378,
        )
    )

    print("\n" + "="*60)
    print("Testing Pinochle Deck 7-card poker calculations...")
    test_deck(
        DeckAnalyzer(num_ranks=6, num_suits=4, num_copies=2, hand_size=7),
        # Pinochle deck with 7-card hands
        # With duplicate copies, pairs become extremely common (100%!)
        # 5oak much more common than in 5-card variant
        ExpectedCounts(
            total = 73629072,
            straight_flushes = 251264,
            five_oaks = 268848,  # Much more common with 7 cards!
            four_oaks = 4418448,
            full_houses = 24249120,
            flushes = 2132064,
            straights = 20987904,
            three_oaks = 33502608,
            two_pairs = 58870560,
            pairs = 73629072,  # 100% - every 7-card hand has at least a pair!
        )
    )

    print("\n" + "="*60)
    print("Testing Fantasy 6-Suit Deck 7-card poker calculations...")
    test_deck(
        DeckAnalyzer(num_ranks=13, num_suits=6, num_copies=1, hand_size=7),
        # Fantasy 6-suit deck with 7-card hands (78 cards total)
        # Flushes remain much rarer than standard due to 6-way suit distribution
        # 5oak becomes more achievable with 7 cards vs 5 cards
        ExpectedCounts(
            total = 2641902120,
            straight_flushes = 153792,
            five_oaks = 200304,  # Still rare but more common with 7 cards
            four_oaks = 11830104,
            full_houses = 100961640,
            flushes = 16741296,  # Still much rarer than standard 7-card (0.63% vs 3.06%)
            straights = 116590752,
            three_oaks = 277209504,
            two_pairs = 784358640,
            pairs = 2161531944,  # 81.8% - pairs less common than standard due to more cards
        )
    )

    print("\n" + "="*60)
    print("All tests completed!")
