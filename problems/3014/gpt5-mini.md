# [Problem 3014: Minimum Number of Pushes to Type Word I](https://leetcode.com/problems/minimum-number-of-pushes-to-type-word-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can remap 8 keys (2-9) arbitrarily and each letter appears exactly once in the word (distinct letters). We want to minimize total presses where position within a key equals number of presses for that letter. Because all letters have equal weight (each appears once), we should give as many letters as possible the smallest possible press count (1), then the next smallest (2), and so on. Each press-count layer can accommodate up to 8 letters (one per key). So for n = len(word), up to 8 letters cost 1, next up to 8 cost 2, etc. No need to consider letter identity or frequency ordering since all frequencies are 1.

## Refining the problem, round 2 thoughts
So the optimal strategy is to fill "layers" of press counts: layer 1 (cost 1) can hold min(8, n) letters, layer 2 holds next min(8, remaining) letters at cost 2, etc. Compute total as sum over layers: layer_index * number_of_letters_in_layer. Edge cases: n <= 8 => answer = n. Complexity is trivial: O(n) time (n <= 26) and O(1) extra space. No need for sorting or DP.

## Attempted solution(s)
```python
class Solution:
    def minimumKeypresses(self, word: str) -> int:
        n = len(word)
        presses = 0
        keys = 8  # keys 2 through 9
        layer = 1
        remaining = n
        while remaining > 0:
            take = min(keys, remaining)
            presses += take * layer
            remaining -= take
            layer += 1
        return presses
```
- Notes:
  - Approach: Greedy filling of press-count layers (1, 2, 3, ...) with up to 8 letters per layer.
  - Time complexity: O(n) where n = len(word) (but n <= 26, so effectively constant).
  - Space complexity: O(1).
  - This works because all letters are distinct and have equal weight (one occurrence), so it's optimal to assign the smallest press counts to any letters until capacity is filled.