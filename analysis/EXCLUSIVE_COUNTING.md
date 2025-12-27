# Exclusive Counting Feature

## Overview

Added an optional `exclusive` parameter to all `count_*` methods in `DeckAnalyzer` to support exclusive counting based on definitional containment.

## What is Exclusive Counting?

**Inclusive counting** (default, `exclusive=False`):
- Counts hands with "at least" the specified pattern
- Example: `count_pairs()` counts all hands with at least one pair (includes two-pair, trips, full house, etc.)

**Exclusive counting** (`exclusive=True`):
- Counts only hands with the specified pattern that are NOT also "better" hands
- "Better" is defined by definitional containment (not poker ranking)
- Example: `count_pairs(exclusive=True)` counts only hands with exactly one pair (excludes two-pair, trips, etc.)

## Definitional Containment Rules

A hand type X "contains" hand type Y if having X necessarily means having Y:

### Containment Hierarchy

```
5-of-a-kind
    └─> 4-of-a-kind
            └─> 3-of-a-kind
                    └─> pair

Full house
    ├─> 3-of-a-kind
    │       └─> pair
    └─> 2-pair
            └─> pair

Straight flush
    ├─> Straight
    └─> Flush
```

### Exclusive Definitions

- **5oak exclusive** = 5oak (no better hands exist)
- **Straight flush exclusive** = straight flush (no better hands exist)
- **Full house exclusive** = full house (no better hands exist)
- **4oak exclusive** = 4oak but not 5oak
- **Straight exclusive** = straight but not straight flush
- **Flush exclusive** = flush but not straight flush
- **3oak exclusive** = 3oak but not {4oak, 5oak, full house}
- **2pair exclusive** = 2pair but not full house
- **Pair exclusive** = pair but not {2pair, 3oak, 4oak, 5oak, full house}

## Important Notes

### Overlaps Still Exist

Exclusive counts can still overlap because some hand types are orthogonal:

- **Flush and Pair**: A flush with a pair is counted in both exclusive categories
- **Straight and Pair**: In larger hands (7+ cards), a straight can coexist with pairs

This is correct behavior! Flush doesn't "contain" pair, and vice versa.

### Not Traditional Poker Ranking

Exclusive counting ≠ traditional poker hand ranking:

- Traditional ranking: Each hand counted in its BEST category only
- Exclusive counting: Hands can appear in multiple orthogonal categories

### Sum Won't Equal Total

Because of overlaps, the sum of all exclusive counts will generally be > total hands.

## API Changes

All counting methods now accept an `exclusive` parameter:

```python
def count_pairs(self, exclusive: bool = False) -> int:
def count_two_pair(self, exclusive: bool = False) -> int:
def count_three_of_kind(self, exclusive: bool = False) -> int:
def count_full_house(self, exclusive: bool = False) -> int:
def count_straights(self, exclusive: bool = False) -> int:
def count_flushes(self, exclusive: bool = False) -> int:
def count_four_of_kind(self, exclusive: bool = False) -> int:
def count_straight_flushes(self, exclusive: bool = False) -> int:
def count_five_of_kind(self, exclusive: bool = False) -> int:
```

## Examples

### Example 1: Standard 5-card poker

```python
analyzer = DeckAnalyzer(num_ranks=13, num_suits=4, num_copies=1, hand_size=5)

# Inclusive: counts all hands with at least a straight (including SF)
straights_inc = analyzer.count_straights(exclusive=False)  # 10,240

# Exclusive: counts only straights that are not straight flushes
straights_exc = analyzer.count_straights(exclusive=True)   # 10,200

# Difference is the straight flush count
sf_count = analyzer.count_straight_flushes()                # 40
assert straights_inc - straights_exc == sf_count
```

### Example 2: Three of a kind

```python
# Inclusive: all hands with at least 3oak
three_oak_inc = analyzer.count_three_of_kind(exclusive=False)  # 59,280

# Exclusive: 3oak but not 4oak, 5oak, or full house
three_oak_exc = analyzer.count_three_of_kind(exclusive=True)   # 54,912

# Difference includes 4oak and full house
four_oak = analyzer.count_four_of_kind()        # 624
full_house = analyzer.count_full_house()        # 3,744
# 624 + 3,744 = 4,368 (the difference)
```

### Example 3: Pinochle deck with 5oak

```python
# Pinochle deck allows 5oak due to duplicate cards
analyzer = DeckAnalyzer(num_ranks=6, num_suits=4, num_copies=2, hand_size=5)

four_oak_inc = analyzer.count_four_of_kind(exclusive=False)  # 17,136
four_oak_exc = analyzer.count_four_of_kind(exclusive=True)   # 16,800
five_oak = analyzer.count_five_of_kind()                      # 336

# Exclusive 4oak excludes hands that also have 5oak
assert four_oak_inc - four_oak_exc == five_oak
```

## Use Cases

### Inclusive Counting
- "What are my odds of getting AT LEAST a pair?"
- "What's the probability of making AT LEAST a flush?"
- Analyzing minimum hand strength

### Exclusive Counting
- "What are my odds of getting EXACTLY a pair (no better)?"
- "What's the probability of a flush that's not a straight flush?"
- Understanding hand distributions without hierarchical overlaps
- Breaking down hands by their specific patterns

## Testing

Run the test suite to verify exclusive counting:

```bash
python3 test_exclusive_counting.py
```

Run the demonstration:

```bash
python3 demo_exclusive.py
```

## Implementation Details

### Partition-Based Hands
For hands counted using partitions (pairs, trips, quads, full house):
- Exclusive logic filters partitions based on their properties
- Example: Exclusive pair only counts partitions with max=2 and exactly one value ≥2

### Straight/Flush Hands
For straights and flushes:
- Exclusive logic subtracts straight flush count
- Handles both 5-card (simple) and 7+ card (inclusion-exclusion) cases

### Code Example
```python
def count_straights(self, exclusive: bool = False) -> int:
    # ... compute total (inclusive count) ...

    if exclusive:
        # Subtract straight flushes
        total -= self.count_straight_flushes()

    return total
```
