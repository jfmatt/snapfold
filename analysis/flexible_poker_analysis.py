"""
Flexible poker hand analysis for any deck configuration.
Works with any combination of ranks, suits, and duplicate copies.

Examples:
- Standard deck: (13 ranks, 4 suits, 1 copy) = 52 cards
- Pinochle deck: (6 ranks, 4 suits, 2 copies) = 48 cards  
- Short-deck poker: (9 ranks, 4 suits, 1 copy) = 36 cards
- Double deck: (13 ranks, 4 suits, 2 copies) = 104 cards
"""

import math
from collections import defaultdict
from functools import cache
from typing import Tuple, List, Dict

class DeckAnalyzer:
    """Analyze poker hands for any deck configuration."""

    def __init__(self, num_ranks: int, num_suits: int, num_copies: int, hand_size: int = 5):
        """
        Initialize deck analyzer.

        Args:
            num_ranks: Number of distinct ranks (e.g., 13 for standard, 6 for pinochle)
            num_suits: Number of suits (typically 4)
            num_copies: Number of copies of each card (1 for standard, 2 for pinochle)
            hand_size: Number of cards in a hand (default 5, use 7 for Texas Hold'em)
        """
        self.num_ranks = num_ranks
        self.num_suits = num_suits
        self.num_copies = num_copies
        self.hand_size = hand_size

        # Derived values
        self.cards_per_rank = num_suits * num_copies
        self.cards_per_suit = num_ranks * num_copies
        self.total_cards = num_ranks * num_suits * num_copies

        # Rank names for display (can be customized)
        if num_ranks == 6:  # Pinochle
            self.rank_names = ['9', '10', 'J', 'Q', 'K', 'A']
        elif num_ranks == 9:  # Short deck
            self.rank_names = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        elif num_ranks == 13:  # Standard
            self.rank_names = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        else:
            self.rank_names = [f'R{i+1}' for i in range(num_ranks)]

    def C(self, n: int, k: int) -> int:
        """Calculate n choose k."""
        if k > n or k < 0:
            return 0
        return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

    @cache
    def generate_partitions(self, n: int, max_val: int = None, max_len: int = None) -> List[List[int]]:
        """Generate all integer partitions of n.

        Args:
            n: The number to partition
            max_val: Maximum value allowed in partition (default: n)
            max_len: Maximum length of partition (default: n)

        Returns:
            List of partitions, each partition is a list of integers in descending order
        """
        if max_val is None:
            max_val = min(n, self.cards_per_rank)
        if max_len is None:
            max_len = min(n, self.num_ranks)

        def partition_helper(target, max_value, max_length):
            if target == 0:
                return [[]]
            if max_length == 0:
                return []

            partitions = []
            for value in range(min(target, max_value), 0, -1):
                for sub_partition in partition_helper(target - value, value, max_length - 1):
                    partitions.append([value] + sub_partition)
            return partitions

        return partition_helper(n, max_val, max_len)

    def count_ways_for_partition(self, partition: List[int]) -> int:
        """Count the number of ways to realize a specific partition.

        Args:
            partition: List of integers representing card counts per rank

        Returns:
            Number of ways to realize this partition with the current deck
        """
        # Group identical values in the partition
        from collections import Counter
        value_counts = Counter(partition)

        # Check if partition is realizable with our deck
        if len(partition) > self.num_ranks:
            return 0
        if any(val > self.cards_per_rank for val in partition):
            return 0

        # Calculate the number of ways
        ways = 1
        remaining_ranks = self.num_ranks

        for value, count in sorted(value_counts.items(), reverse=True):
            if value == 0:
                continue
            # Choose 'count' ranks from remaining ranks
            ways *= self.C(remaining_ranks, count)
            remaining_ranks -= count
            # For each chosen rank, choose 'value' cards from cards_per_rank
            ways *= self.C(self.cards_per_rank, value) ** count

        # Multinomial coefficient for arranging the groups
        # (This is already handled by the C(remaining_ranks, count) above)

        return ways

    def get_deck_description(self) -> str:
        """Get a description of the deck configuration."""
        deck_names = {
            (13, 4, 1): "Standard Deck",
            (6, 4, 2): "Pinochle Deck",
            (9, 4, 1): "Short-Deck Poker",
            (13, 4, 2): "Double Deck"
        }
        name = deck_names.get((self.num_ranks, self.num_suits, self.num_copies), "Custom Deck")
        return f"{name} ({self.num_ranks} ranks × {self.num_suits} suits × {self.num_copies} copies = {self.total_cards} cards)"

    def count_total_hands(self) -> int:
        """Count total possible hands."""
        return self.C(self.total_cards, self.hand_size)

    def count_pairs(self) -> int:
        """Count hands with at least one pair."""
        # Generate all partitions of hand_size
        partitions = self.generate_partitions(self.hand_size)

        # Sum ways for partitions with at least one value >= 2
        count = 0
        for partition in partitions:
            if any(val >= 2 for val in partition):
                count += self.count_ways_for_partition(partition)

        return count

    def count_two_pair(self) -> int:
        """Count hands with at least two pairs (of different ranks)."""
        if self.hand_size < 4:
            return 0  # Need at least 4 cards for two pairs

        # Generate all partitions of hand_size
        partitions = self.generate_partitions(self.hand_size)

        # Sum ways for partitions with at least two different ranks having >= 2 cards
        count = 0
        for partition in partitions:
            has_two_pair = sum(1 for val in partition if val >= 2) >= 2
            if has_two_pair:
                count += self.count_ways_for_partition(partition)

        return count

    def count_three_of_kind(self) -> int:
        """Count hands with at least three of a kind."""
        if self.hand_size < 3:
            return 0  # Need at least 3 cards for three of a kind

        # Generate all partitions of hand_size
        partitions = self.generate_partitions(self.hand_size)

        # Sum ways for partitions with at least one value >= 3
        count = 0
        for partition in partitions:
            if any(val >= 3 for val in partition):
                count += self.count_ways_for_partition(partition)

        return count

    def count_full_house(self) -> int:
        """Count hands with a full house (3 of one rank, 2 of another)."""
        if self.num_ranks < 2 or self.hand_size < 5:
            return 0  # Need at least 2 ranks and 5 cards for a full house

        # Generate all partitions of hand_size
        partitions = self.generate_partitions(self.hand_size)

        # Sum ways for partitions containing at least one 3 and at least one 2
        count = 0
        for partition in partitions:
            has_triple = any(val >= 3 for val in partition)
            has_two_pair = sum(1 for val in partition if val >= 2) >= 2

            if has_triple and has_two_pair:
                count += self.count_ways_for_partition(partition)

        return count

    def count_straights(self) -> int:
        """Count hands that contain a straight."""
        if self.num_ranks < 5 or self.hand_size < 5:
            return 0

        # Number of possible 5-card straight sequences
        num_straight_types = self.num_ranks - 4

        # Add ace-low straight (A-2-3-4-5)
        num_straight_types += 1

        # For each straight type, choose 1 card from each of 5 consecutive ranks
        # Then choose remaining cards from the rest of the deck
        remaining = self.hand_size - 5
        straight_ways = num_straight_types * (self.cards_per_rank ** 5)

        if remaining > 0:
            # For simplicity, we allow any remaining cards from the deck
            # (This may include cards that complete the same straight)
            remaining_cards = self.total_cards - 5 * self.cards_per_rank
            if remaining_cards >= remaining:
                straight_ways *= self.C(remaining_cards, remaining)

        return straight_ways

    def count_flushes(self) -> int:
        """Count hands that contain a flush (at least 5 cards of the same suit)."""
        if self.cards_per_suit < 5 or self.hand_size < 5:
            return 0

        flush_ways = self.num_suits * self.C(self.cards_per_suit, 5)

        if self.hand_size > 5:
            remaining_cards = self.total_cards - 5
            flush_ways *= self.C(remaining_cards, self.hand_size - 5)

        return flush_ways

    def count_four_of_kind(self) -> int:
        """Count hands with at least four of a kind."""
        if self.hand_size < 4 or self.cards_per_rank < 4:
            return 0  # Need at least 4 cards in hand and 4 cards per rank

        # Generate all partitions of hand_size
        partitions = self.generate_partitions(self.hand_size)

        # Sum ways for partitions with at least one value >= 4
        count = 0
        for partition in partitions:
            if any(val >= 4 for val in partition):
                count += self.count_ways_for_partition(partition)

        return count

    def count_straight_flushes(self) -> int:
        """Count hands that are both straight and flush."""
        if self.num_ranks < 5 or self.cards_per_suit < 5 or self.hand_size < 5:
            return 0

        # Number of possible straight sequences
        num_straight_types = self.num_ranks - 4

        # Add ace-low straight
        num_straight_types += 1

        # For each suit and straight type, choose the 5 specific cards
        # For pinochle with 2 copies: each card has 2 choices
        remaining = self.hand_size - 5
        sf_ways = self.num_suits * num_straight_types * (self.num_copies ** 5)

        if remaining > 0:
            # Choose remaining cards from the rest of the deck
            # (excluding the 5 cards in the straight flush)
            remaining_cards = self.total_cards - 5 * self.num_copies
            if remaining_cards >= remaining:
                sf_ways *= self.C(remaining_cards, remaining)

        return sf_ways

    def count_five_of_kind(self) -> int:
        """Count hands with at least five of a kind."""
        if self.cards_per_rank < 5 or self.hand_size < 5:
            return 0

        # Generate all partitions of hand_size
        partitions = self.generate_partitions(self.hand_size)

        # Sum ways for partitions with at least one value >= 5
        count = 0
        for partition in partitions:
            if any(val >= 5 for val in partition):
                count += self.count_ways_for_partition(partition)

        return count

    def analyze_hands(self) -> Dict[str, Tuple[int, float]]:
        """Analyze all hand types and return counts and probabilities."""
        total_hands = self.count_total_hands()

        results = {}

        # Calculate all hand types
        hand_counts = [
            ("At least one pair", self.count_pairs()),
            ("At least two pair", self.count_two_pair()),
            ("At least 3 of a kind", self.count_three_of_kind()),
            ("Full house", self.count_full_house()),
            ("Straight", self.count_straights()),
            ("Flush", self.count_flushes()),
            ("At least 4 of a kind", self.count_four_of_kind()),
            ("Straight flush", self.count_straight_flushes()),
            ("5 of a kind", self.count_five_of_kind())
        ]

        for hand_type, count in hand_counts:
            prob = count / total_hands if total_hands > 0 else 0
            results[hand_type] = (count, prob)

        return results

    def print_analysis(self):
        """Print comprehensive analysis of the deck."""
        print(f"\n{self.get_deck_description()}")
        print(f"Hand size: {self.hand_size} cards")

        total_hands = self.count_total_hands()
        print(f"Total possible hands: {total_hands:,}")

        print(f"\nDeck properties:")
        print(f"  - Cards per rank: {self.cards_per_rank}")
        print(f"  - Cards per suit: {self.cards_per_suit}")

        results = self.analyze_hands()

        print()
        print("HAND TYPE COUNTS (with overlaps)")

        for hand_type, (count, prob) in results.items():
            if count > 0:  # Only show possible hands
                print(f"{hand_type:<25} {count:>10,} hands  ({prob:>7.2%})")

        # Calculate total probability
        total_prob = sum(prob for _, prob in results.values())
        print(f"\nSum of probabilities: {total_prob:.1%} (overlaps cause >100%)")

        print()
        print("RARITY RANKING (rarest to most common)")

        sorted_results = sorted(
            [(k, v) for k, v in results.items() if v[0] > 0],
            key=lambda x: x[1][0]
        )

        for i, (hand_type, (count, prob)) in enumerate(sorted_results, 1):
            ratio = f"1 in {total_hands/count:,.0f}" if count > 0 else "N/A"
            print(f"{i}. {hand_type:<25} {prob:>7.4%}  ({ratio})")


def main():
    """Main function to demonstrate the analyzer."""
    # Analyze standard deck with 5 cards (traditional poker)
    print("\n" + "~" * 80)
    print("STANDARD DECK - 5 CARDS (Traditional Poker)")
    print("~" * 80)
    standard = DeckAnalyzer(num_ranks=13, num_suits=4, num_copies=1, hand_size=5)
    standard.print_analysis()

    # Analyze standard deck with 7 cards (Texas Hold'em)
    print("\n" + "~" * 80)
    print("STANDARD DECK - 7 CARDS (Texas Hold'em)")
    print("~" * 80)
    holdem = DeckAnalyzer(num_ranks=13, num_suits=4, num_copies=1, hand_size=7)
    holdem.print_analysis()

    # Analyze pinochle deck with 5 cards
    print("\n" + "~" * 80)
    print("PINOCHLE DECK - 5 CARDS")
    print("~" * 80)
    pinochle = DeckAnalyzer(num_ranks=6, num_suits=4, num_copies=2, hand_size=5)
    pinochle.print_analysis()

    # Analyze short deck with 5 cards
    print("\n" + "~" * 80)
    print("SHORT-DECK - 5 CARDS")
    print("~" * 80)
    short_deck = DeckAnalyzer(num_ranks=9, num_suits=4, num_copies=1, hand_size=5)
    short_deck.print_analysis()

    # Analyze short deck with 7 cards
    print("\n" + "~" * 80)
    print("SHORT-DECK HOLDEM - 7 CARDS")
    print("~" * 80)
    short_deck_he = DeckAnalyzer(num_ranks=9, num_suits=4, num_copies=1, hand_size=7)
    short_deck_he.print_analysis()


if __name__ == "__main__":
    main()
