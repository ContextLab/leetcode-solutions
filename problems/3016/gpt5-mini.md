# [Problem 3016: Minimum Number of Pushes to Type Word II](https://leetcode.com/problems/minimum-number-of-pushes-to-type-word-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can remap 26 letters to the 8 keys (2..9). Each key can hold any number of letters, but the cost to type a letter equals its position on its key (1 for first, 2 for second, ...). For a given press-count j, there are at most 8 letters that can be placed at cost j (one per key). So the "slots" of cost 1 are 8, cost 2 are 8, etc. To minimize total pushes, higher-frequency letters should occupy lower-cost slots. That suggests sorting letters by frequency descending and assigning them to slots from lowest cost upward. This is a greedy assignment: take the most frequent letters and put them in cost-1 slots (up to 8), then the next in cost-2 slots, etc.

## Refining the problem, round 2 thoughts
- We only care about letter frequencies (26 possible letters), not their order.
- Optimality: an exchange argument shows it's always better to assign higher-frequency letters to smaller-cost slots; because swapping a higher-frequency letter into a lower-cost slot reduces or keeps total cost.
- Edge cases: fewer than 8 distinct letters (all cost 1). Very large word length (up to 1e5) — need linear-time counting.
- Complexity: counting frequencies O(n) where n = len(word), sorting at most 26 frequencies is constant-time effectively O(26 log 26) ~ O(1). So overall O(n) time, O(1) extra space (besides input and frequency array).

## Attempted solution(s)
```python
from collections import Counter
from typing import List

class Solution:
    def minimumNumberOfPushes(self, word: str) -> int:
        """
        Return the minimum number of key pushes to type the given word
        after optimally remapping letters to the 8 keys (2-9).
        """
        # Count frequencies of each letter
        freq_counts: List[int] = list(Counter(word).values())
        # Sort frequencies descending: highest frequency get smallest cost slots
        freq_counts.sort(reverse=True)
        
        total_pushes = 0
        # There are 8 keys, so for index i (0-based), cost = (i // 8) + 1
        for i, f in enumerate(freq_counts):
            total_pushes += ((i // 8) + 1) * f
        
        return total_pushes
```
- Notes:
  - Approach: Greedy by frequency. There are 8 slots with cost 1 (one per key), then 8 slots with cost 2, etc. Sort frequencies descending and assign in that order.
  - Time complexity: O(n) to count frequencies + O(26 log 26) to sort the 26 counts, so overall O(n).
  - Space complexity: O(1) extra (frequency array of size ≤ 26).