# [Problem 1079: Letter Tile Possibilities](https://leetcode.com/problems/letter-tile-possibilities/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count all distinct non-empty sequences I can form from the given tiles. Tiles can repeat, and permutations that are identical because of repeated letters should be counted only once. A brute force idea is to generate all permutations of all lengths and deduplicate (e.g., using a set). That would work for n up to 7 but generating and deduplicating all permutations explicitly might be wasteful.

A common approach for problems with repeated items is to use counts (a multiset) and backtrack: at each step, choose one available letter (decrement its count), form a new sequence (count it), then recurse to extend it further; after recursion backtrack (restore count). This way duplicates are implicitly handled because we only choose by letter type and respect counts. Since n ≤ 7 this exponential approach is perfectly fine.

## Refining the problem, round 2 thoughts
- Use a Counter / frequency array of letters to represent available tiles.
- Backtracking: for each letter with count > 0:
  - decrement count,
  - increment global answer by 1 (we formed one new non-empty sequence by appending that letter),
  - recurse to form longer sequences,
  - increment count back (backtrack).
- No need to store sequences themselves (just count them), so memory is small.
- Complexity: we explore each distinct sequence once. The total number of sequences is sum_{k=1..n} permutations of length k accounting for duplicates; worst-case when all letters distinct it's sum_{k=1..n} n!/(n-k)!, which is O(n!); with n ≤ 7 this is fine.
- Edge cases: single letter (returns 1), all identical letters (returns n because you can form sequences of length 1..n but only one distinct sequence per length).

## Attempted solution(s)
```python
from collections import Counter

class Solution:
    def numTilePossibilities(self, tiles: str) -> int:
        """
        Count distinct non-empty sequences that can be formed from tiles.
        Backtracking over letter counts (multiset).
        """
        counts = Counter(tiles)
        self.ans = 0

        def backtrack():
            # Try using each available letter as the next character
            for ch in counts:
                if counts[ch] == 0:
                    continue
                # Use this letter to form a new sequence (count it)
                self.ans += 1
                counts[ch] -= 1
                backtrack()
                counts[ch] += 1

        backtrack()
        return self.ans
```
- Approach notes: Use a Counter to track remaining tiles, and backtrack by choosing each letter that still has count > 0. Each time we pick a letter we have formed one new distinct sequence (so increment count), and we continue to extend it recursively.
- Time complexity: Exponential in n. More precisely the number of recursive calls equals the number of distinct non-empty sequences, which in the worst case (all letters distinct) is sum_{k=1..n} n!/(n-k)! = O(n!). With n ≤ 7 this is small enough.
- Space complexity: O(1) extra besides the recursion stack and the Counter; recursion depth ≤ n so O(n) stack. The Counter uses up to 26 entries (or at most n distinct letters).