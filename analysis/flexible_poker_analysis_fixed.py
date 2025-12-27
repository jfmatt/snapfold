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

    def count_pairs(self, exclusive: bool = False) -> int:
        """Count hands with at least one pair.

        Args:
            exclusive: If True, only count pairs that are not also 2pair, 3oak, 4oak, 5oak, or full house.
        """
        # Generate all partitions of hand_size
        partitions = self.generate_partitions(self.hand_size)

        # Sum ways for partitions with at least one value >= 2
        count = 0
        for partition in partitions:
            has_pair = any(val >= 2 for val in partition)

            if exclusive:
                # Exclude hands that are also better hand types
                has_two_pair = sum(1 for val in partition if val >= 2) >= 2
                has_3oak = any(val >= 3 for val in partition)

                if has_pair and not has_two_pair and not has_3oak:
                    count += self.count_ways_for_partition(partition)
            else:
                if has_pair:
                    count += self.count_ways_for_partition(partition)

        return count

    def count_two_pair(self, exclusive: bool = False) -> int:
        """Count hands with at least two pairs (of different ranks).

        Args:
            exclusive: If True, only count two pair that is not also a full house.
        """
        if self.hand_size < 4:
            return 0  # Need at least 4 cards for two pairs

        # Generate all partitions of hand_size
        partitions = self.generate_partitions(self.hand_size)

        # Sum ways for partitions with at least two different ranks having >= 2 cards
        count = 0
        for partition in partitions:
            has_two_pair = sum(1 for val in partition if val >= 2) >= 2

            if exclusive:
                # Exclude hands that are also full house
                has_3oak = any(val >= 3 for val in partition)
                has_full_house = has_3oak and has_two_pair

                if has_two_pair and not has_full_house:
                    count += self.count_ways_for_partition(partition)
            else:
                if has_two_pair:
                    count += self.count_ways_for_partition(partition)

        return count

    def count_three_of_kind(self, exclusive: bool = False) -> int:
        """Count hands with at least three of a kind.

        Args:
            exclusive: If True, only count 3oak that is not also 4oak, 5oak, or full house.
        """
        if self.hand_size < 3:
            return 0  # Need at least 3 cards for three of a kind

        # Generate all partitions of hand_size
        partitions = self.generate_partitions(self.hand_size)

        # Sum ways for partitions with at least one value >= 3
        count = 0
        for partition in partitions:
            has_3oak = any(val >= 3 for val in partition)

            if exclusive:
                # Exclude hands that are also 4oak, 5oak, or full house
                has_4oak = any(val >= 4 for val in partition)
                has_two_pair = sum(1 for val in partition if val >= 2) >= 2
                has_full_house = has_3oak and has_two_pair

                if has_3oak and not has_4oak and not has_full_house:
                    count += self.count_ways_for_partition(partition)
            else:
                if has_3oak:
                    count += self.count_ways_for_partition(partition)

        return count

    def count_full_house(self, exclusive: bool = False) -> int:
        """Count hands with a full house (3 of one rank, 2 of another).

        Args:
            exclusive: No effect (no hand definitionally contains full house).
        """
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

        # Exclusive = inclusive for full house (no better hands)
        return count

    def count_straights(self, exclusive: bool = False) -> int:
        """Count hands that contain a straight.

        For hands larger than 5 cards, we need to avoid double-counting different straights.
        Uses inclusion-exclusion to count hands with at least one card from each required rank.

        Args:
            exclusive: If True, only count straights that are not also straight flushes.
        """
        if self.num_ranks < 5 or self.hand_size < 5:
            return 0

        total = 0
        remaining_cards = self.hand_size - 5

        # Number of possible straight types
        num_straight_types = self.num_ranks - 3 # assumes ace can be low

        if remaining_cards == 0:
            # Simple case: exactly 5 cards
            # Include ace-low
            total = num_straight_types * (self.cards_per_rank ** 5)

            if exclusive:
                # Subtract straight flushes
                total -= self.count_straight_flushes()

            return total

        # For larger hands, use inclusion-exclusion
        # Strategy: assign each hand to its HIGHEST straight by excluding next rank

        # Handle non-ace-high straights (can be extended upward)
        for straight_idx in range(num_straight_types - 1):
            # Count hands with at least 1 card from each of the 5 straight ranks
            # and NO cards from the next rank up (to avoid double-counting)

            # Use inclusion-exclusion:
            # Total hands from (52 - 4) cards = C(48, 7)
            # Minus hands missing at least one required rank

            ranks_in_straight = 5
            excluded_rank = 1  # The next rank up
            available_ranks = self.num_ranks - ranks_in_straight - excluded_rank
            cards_per_rank = self.cards_per_rank

            # Count hands with cards only from the allowed ranks
            # (the 5 straight ranks + other ranks, but NOT the next rank up)
            total_allowed_cards = (ranks_in_straight + available_ranks) * cards_per_rank

            # All possible hands from allowed cards
            all_from_allowed = self.C(total_allowed_cards, self.hand_size)

            # Subtract hands missing at least one required rank using inclusion-exclusion
            # Sum over k = 1 to 5: (-1)^k * C(5, k) * C(total_allowed_cards - k*cards_per_rank, hand_size)
            count_with_all_ranks = all_from_allowed
            for k in range(1, ranks_in_straight + 1):
                cards_without_k_ranks = total_allowed_cards - k * cards_per_rank
                if cards_without_k_ranks >= self.hand_size:
                    count_with_all_ranks += ((-1) ** k) * self.C(ranks_in_straight, k) * self.C(cards_without_k_ranks, self.hand_size)

            total += count_with_all_ranks

        # Handle ace-high straight (cannot be extended)
        ranks_in_straight = 5
        available_ranks = self.num_ranks - ranks_in_straight
        total_allowed_cards = self.total_cards  # Can use any rank

        all_from_allowed = self.C(total_allowed_cards, self.hand_size)
        count_with_all_ranks = all_from_allowed
        for k in range(1, ranks_in_straight + 1):
            cards_without_k_ranks = total_allowed_cards - k * self.cards_per_rank
            if cards_without_k_ranks >= self.hand_size:
                count_with_all_ranks += ((-1) ** k) * self.C(ranks_in_straight, k) * self.C(cards_without_k_ranks, self.hand_size)

        total += count_with_all_ranks

        if exclusive:
            # Subtract straight flushes
            total -= self.count_straight_flushes()

        return total

    def count_flushes(self, exclusive: bool = False) -> int:
        """Count hands that contain a flush (at least 5 cards of the same suit).

        For larger hands, we count all possible ways to get at least 5 of the same suit.

        Args:
            exclusive: If True, only count flushes that are not also straight flushes.
        """
        if self.cards_per_suit < 5 or self.hand_size < 5:
            return 0

        total = 0

        # For each suit
        for suit in range(self.num_suits):
            # For each possible number of cards from this suit (5 to min(hand_size, cards_per_suit))
            max_from_suit = min(self.hand_size, self.cards_per_suit)

            for num_from_suit in range(5, max_from_suit + 1):
                # Choose num_from_suit cards from this suit
                ways = self.C(self.cards_per_suit, num_from_suit)

                # Choose remaining cards from other suits
                remaining = self.hand_size - num_from_suit
                if remaining > 0:
                    other_suit_cards = (self.num_suits - 1) * self.cards_per_suit
                    ways *= self.C(other_suit_cards, remaining)

                total += ways

        if exclusive:
            # Subtract straight flushes
            total -= self.count_straight_flushes()

        return total

    def count_four_of_kind(self, exclusive: bool = False) -> int:
        """Count hands with at least four of a kind.

        Args:
            exclusive: If True, only count 4oak that is not also 5oak.
        """
        if self.hand_size < 4 or self.cards_per_rank < 4:
            return 0  # Need at least 4 cards in hand and 4 cards per rank

        # Generate all partitions of hand_size
        partitions = self.generate_partitions(self.hand_size)

        # Sum ways for partitions with at least one value >= 4
        count = 0
        for partition in partitions:
            has_4oak = any(val >= 4 for val in partition)

            if exclusive:
                # Exclude hands that are also 5oak
                has_5oak = any(val >= 5 for val in partition)

                if has_4oak and not has_5oak:
                    count += self.count_ways_for_partition(partition)
            else:
                if has_4oak:
                    count += self.count_ways_for_partition(partition)

        return count

    def count_straight_flushes(self, exclusive: bool = False) -> int:
        """Count hands that are both straight and flush.

        Args:
            exclusive: No effect (no hand definitionally contains straight flush).

        For hands larger than 5 cards, avoid double-counting different straight flushes.
        """
        if self.num_ranks < 5 or self.cards_per_suit < 5 or self.hand_size < 5:
            return 0

        total = 0
        remaining_cards = self.hand_size - 5

        # Number of possible straight types (including ace-low)
        num_straight_types = self.num_ranks - 3  # assumes ace can be low

        if remaining_cards == 0:
            # Simple case: exactly 5 cards
            # Each suit can have num_straight_types different straights (including ace-low)
            return self.num_suits * num_straight_types * (self.num_copies ** 5)

        # For each suit
        # Handle ace-low straight (A-2-3-4-5 or A-6-7-8-9) if it exists
        # Ace-low can be extended upward
        ways = self.num_copies ** 5
        # Ace-low can be extended by the next rank up (rank after the 5th lowest)
        excluded_cards = self.num_copies
        available_cards = self.total_cards - 5 * self.num_copies - excluded_cards
        if available_cards >= remaining_cards:
            ways *= self.C(available_cards, remaining_cards)
            total += ways

        # Handle middle straights (can be extended upward)
        # These are all straights except ace-low and ace-high
        # For 13 ranks: 2-3-4-5-6, 3-4-5-6-7, ..., 9-10-J-Q-K
        # That's (num_straight_types - 2) straights
        num_middle_straights = num_straight_types - 2
        for straight_idx in range(num_middle_straights):
            # We have exactly one way to pick the 5 cards for this SF
            ways = self.num_copies ** 5  # For decks with multiple copies per card

            # These straights can be extended upward by one rank
            # So exclude that one card from the same suit
            excluded_cards = self.num_copies  # The card that would extend it upward

            # Choose remaining cards from available cards
            available_cards = self.total_cards - 5 * self.num_copies - excluded_cards
            if available_cards >= remaining_cards:
                ways *= self.C(available_cards, remaining_cards)
                total += ways

        # Handle ace-high straight (10-J-Q-K-A or similar) - cannot be extended upward
        ways = self.num_copies ** 5
        # Ace-high cannot be extended (no card above ace)
        available_cards = self.total_cards - 5 * self.num_copies
        if available_cards >= remaining_cards:
            ways *= self.C(available_cards, remaining_cards)
            total += ways

        # Exclusive = inclusive for straight flush (no better hands)
        return total * self.num_suits

    def count_five_of_kind(self, exclusive: bool = False) -> int:
        """Count hands with at least five of a kind.

        Args:
            exclusive: No effect (no hand definitionally contains 5oak).
        """
        if self.cards_per_rank < 5 or self.hand_size < 5:
            return 0

        # Generate all partitions of hand_size
        partitions = self.generate_partitions(self.hand_size)

        # Sum ways for partitions with at least one value >= 5
        count = 0
        for partition in partitions:
            if any(val >= 5 for val in partition):
                count += self.count_ways_for_partition(partition)

        # Exclusive = inclusive for 5oak (no better hands)
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

    # Analyze pinochle deck with 5 cards
    print("\n" + "~" * 80)
    print("PINOCHLE HOLDEM - 7 CARDS")
    print("~" * 80)
    pinochle_he = DeckAnalyzer(num_ranks=6, num_suits=4, num_copies=2, hand_size=7)
    pinochle_he.print_analysis()

    # Analyze wide deck with many suits
    print("\n" + "~" * 80)
    print("WIDE DECK - 5 CARDS")
    print("~" * 80)
    wide = DeckAnalyzer(num_ranks=13, num_suits=12, num_copies=1, hand_size=5)
    wide.print_analysis()

    # Analyze wide deck with 7 cards
    print("\n" + "~" * 80)
    print("WIDE DECK HOLDEM - 7 CARDS")
    print("~" * 80)
    wide_he = DeckAnalyzer(num_ranks=13, num_suits=12, num_copies=1, hand_size=7)
    wide_he.print_analysis()


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
