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
from typing import Tuple, List, Dict

class DeckAnalyzer:
    """Analyze poker hands for any deck configuration."""

    def __init__(self, num_ranks: int, num_suits: int, num_copies: int):
        """
        Initialize deck analyzer.

        Args:
            num_ranks: Number of distinct ranks (e.g., 13 for standard, 6 for pinochle)
            num_suits: Number of suits (typically 4)
            num_copies: Number of copies of each card (1 for standard, 2 for pinochle)
        """
        self.num_ranks = num_ranks
        self.num_suits = num_suits
        self.num_copies = num_copies

        # Derived values
        self.cards_per_rank = num_suits * num_copies
        self.cards_per_suit = num_ranks * num_copies
        self.total_cards = num_ranks * num_suits * num_copies
        self.hand_size = 5

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
        total = self.count_total_hands()
        # No pairs: choose 5 different ranks, 1 card from each
        no_pairs = self.C(self.num_ranks, self.hand_size) * (self.cards_per_rank ** self.hand_size)
        return total - no_pairs

    def count_two_pair(self) -> int:
        """Count hands with at least two pairs."""
        count = 0

        # Pattern (2,2,1): Exactly two pairs + singleton
        if self.num_ranks >= 3:
            count += self.C(self.num_ranks, 2) * self.C(self.cards_per_rank, 2) * \
                     self.C(self.cards_per_rank, 2) * (self.num_ranks - 2) * self.cards_per_rank

        # Pattern (3,2): Full house (use corrected formula)
        if self.num_ranks >= 2:
            count += self.num_ranks * (self.num_ranks - 1) * \
                     self.C(self.cards_per_rank, 3) * self.C(self.cards_per_rank, 2)

        # Pattern (4,1): Four of a kind + singleton
        if self.num_ranks >= 2 and self.cards_per_rank >= 4:
            # Use the corrected 4oak formula
            remaining_cards = self.total_cards - self.cards_per_rank
            count += self.C(self.num_ranks, 1) * self.C(self.cards_per_rank, 4) * remaining_cards

        # Pattern (5): Five of a kind
        if self.num_ranks >= 1 and self.cards_per_rank >= 5:
            count += self.C(self.num_ranks, 1) * self.C(self.cards_per_rank, 5)

        return count

    def count_three_of_kind(self) -> int:
        """Count hands with at least three of a kind."""
        count = 0

        # Pattern (3,1,1): Three of a kind + two singletons
        if self.num_ranks >= 3:
            # Choose 1 rank for triple, then 2 ranks for singletons
            count += self.num_ranks * self.C(self.num_ranks - 1, 2) * \
                     self.C(self.cards_per_rank, 3) * self.cards_per_rank * self.cards_per_rank

        # Pattern (3,2): Full house (use corrected formula)
        if self.num_ranks >= 2:
            count += self.num_ranks * (self.num_ranks - 1) * \
                     self.C(self.cards_per_rank, 3) * self.C(self.cards_per_rank, 2)

        # Pattern (4,1): Four of a kind + singleton
        if self.num_ranks >= 2 and self.cards_per_rank >= 4:
            remaining_cards = self.total_cards - self.cards_per_rank
            count += self.C(self.num_ranks, 1) * self.C(self.cards_per_rank, 4) * remaining_cards

        # Pattern (5): Five of a kind
        if self.num_ranks >= 1 and self.cards_per_rank >= 5:
            count += self.C(self.num_ranks, 1) * self.C(self.cards_per_rank, 5)

        return count

    def count_full_house(self) -> int:
        """Count hands with a full house (3 of one rank, 2 of another)."""
        if self.num_ranks < 2:
            return 0

        # Choose 1 rank for the triple, then 1 different rank for the pair
        # Order matters: triple rank is distinct from pair rank
        count = self.num_ranks * (self.num_ranks - 1) * \
                self.C(self.cards_per_rank, 3) * self.C(self.cards_per_rank, 2)

        # Note: 5 of a kind could be considered a "degenerate" full house in some games
        # but we don't include it here as it's tracked separately

        return count

    def count_straights(self) -> int:
        """Count hands that contain a straight."""
        if self.num_ranks < 5:
            return 0

        # Number of possible 5-card straight sequences
        num_straight_types = self.num_ranks - 4

        # Add ace-low straight (A-2-3-4-5) for standard/long decks
        # This applies when we have standard ranks (13) or more
        if self.num_ranks >= 13:
            num_straight_types += 1  # Add the ace-low straight

        # For each straight type, choose 1 card from each of 5 consecutive ranks
        return num_straight_types * (self.cards_per_rank ** 5)

    def count_flushes(self) -> int:
        """Count hands where all 5 cards are the same suit."""
        if self.cards_per_suit < 5:
            return 0
        return self.num_suits * self.C(self.cards_per_suit, 5)

    def count_four_of_kind(self) -> int:
        """Count hands with at least four of a kind."""
        count = 0

        # Pattern (4,1): Four of a kind + singleton
        if self.num_ranks >= 2 and self.cards_per_rank >= 4:
            # Choose 1 rank for the 4oak
            # Choose 4 cards from that rank
            # Choose 1 card from the remaining cards
            remaining_cards = self.total_cards - self.cards_per_rank
            count += self.C(self.num_ranks, 1) * self.C(self.cards_per_rank, 4) * remaining_cards

        # Pattern (5): Five of a kind
        if self.num_ranks >= 1 and self.cards_per_rank >= 5:
            count += self.C(self.num_ranks, 1) * self.C(self.cards_per_rank, 5)

        return count

    def count_straight_flushes(self) -> int:
        """Count hands that are both straight and flush."""
        if self.num_ranks < 5 or self.cards_per_suit < 5:
            return 0

        # Number of possible straight sequences
        num_straight_types = self.num_ranks - 4

        # Add ace-low straight for standard/long decks
        if self.num_ranks >= 13:
            num_straight_types += 1

        # For standard deck with 1 copy: each suit has exactly 1 straight flush per straight type
        # For pinochle with 2 copies: each suit has 2^5 ways to form each straight
        return self.num_suits * num_straight_types * (self.num_copies ** 5)

    def count_five_of_kind(self) -> int:
        """Count hands with exactly five of a kind."""
        if self.cards_per_rank < 5:
            return 0
        return self.C(self.num_ranks, 1) * self.C(self.cards_per_rank, 5)

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
    # Analyze pinochle deck
    print("\n" + "~" * 80)
    print("PINOCHLE DECK")
    print("~" * 80)
    pinochle = DeckAnalyzer(num_ranks=6, num_suits=4, num_copies=2)
    pinochle.print_analysis()

    # Analyze standard deck
    print("\n" + "~" * 80)
    print("STANDARD DECK")
    print("~" * 80)
    standard = DeckAnalyzer(num_ranks=13, num_suits=4, num_copies=1)
    standard.print_analysis()

    # Analyze short deck
    print("\n" + "~" * 80)
    print("SHORT-DECK")
    print("~" * 80)
    short_deck = DeckAnalyzer(num_ranks=9, num_suits=4, num_copies=1)
    short_deck.print_analysis()


if __name__ == "__main__":
    main()
