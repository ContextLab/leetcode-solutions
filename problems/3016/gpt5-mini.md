# [Problem 3016: Minimum Number of Pushes to Type Word II](https://leetcode.com/problems/minimum-number-of-pushes-to-type-word-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I will provide a short, high-level summary of the approach rather than inner chain-of-thought. The key observation is that each key (2–9) can supply one letter at each press-count position (1st press, 2nd press, ...). Thus for press-count p there are at most 8 letters that can be assigned that press-count. To minimize total pushes, assign the most frequent letters the smallest press-counts. So sort letter frequencies descending and assign press-count = floor(index/8)+1.

## Refining the problem, round 2 thoughts
- Count frequencies of each letter in the word.
- Sort frequencies descending.
- For the i-th letter in this sorted list (0-based), its press-count = i // 8 + 1.
- Sum freq * press-count.
- Edge cases: fewer than 8 unique letters (all get press-count 1); up to 26 letters so straightforward.
- Time complexity: O(n + U log U) where n = len(word) and U <= 26; effectively O(n). Space: O(1) extra beyond counts.

## Attempted solution(s)
```python
from collections import Counter

class Solution:
    def minimumPresses(self, word: str) -> int:
        # Count frequency of each letter
        freq = Counter(word)
        # Sort frequencies in descending order
        freqs_sorted = sorted(freq.values(), reverse=True)
        total = 0
        # Assign press-counts: up to 8 letters per press-count level
        for i, f in enumerate(freqs_sorted):
            presses = i // 8 + 1
            total += f * presses
        return total
```
- Notes:
  - Approach: greedy assignment of smallest press-counts to highest frequencies.
  - Correctness: For each press-count level p there are at most 8 keys, so the optimal strategy is to fill lower press-count levels with the highest frequencies — a classic rearrangement/greedy argument.
  - Time complexity: O(n) to build counts plus sorting up to 26 items -> O(n). Space complexity: O(1) extra beyond the input and frequency map (bounded by 26).