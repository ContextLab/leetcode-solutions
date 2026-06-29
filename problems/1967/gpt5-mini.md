# [Problem 1967: Number of Strings That Appear as Substrings in Word](https://leetcode.com/problems/number-of-strings-that-appear-as-substrings-in-word/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count how many strings in patterns appear as contiguous substrings of word. The simplest idea is: for each pattern, check if it's a substring of word. In Python that's as easy as `if p in word:` which uses an efficient substring search under the hood. Given constraints are small (patterns up to 100, each length up to 100, word up to 100), this brute-force per-pattern check is perfectly fine.

Another thought: we could precompute all substrings of word into a set and then check membership for each pattern in O(1), but that costs O(W^2) time/space to build the set (W ≤ 100 so still fine). For clarity and simplicity the per-pattern `in` check is easiest and clear.

Also note duplicates in patterns are counted separately (example 3), so we must not deduplicate patterns.

## Refining the problem, round 2 thoughts
- Edge cases: patterns may contain duplicates — count each occurrence separately if it appears in word.
- Very small inputs make any reasonable approach acceptable.
- Complexity: checking each pattern with Python `in` is typically linear in word length times pattern length in worst-case, but with constraints this is trivial.
- Alternative approach (set of substrings): build all substrings of word (O(W^2) substrings) then check pattern membership in O(len(pattern)) to hash — good when many patterns or repeated queries, but not necessary here.

I'll implement the straightforward per-pattern `in` approach inside the LeetCode-style Solution class.

## Attempted solution(s)
```python
class Solution:
    def numOfStrings(self, patterns: list[str], word: str) -> int:
        """
        Count how many strings in patterns appear as substrings in word.
        Each pattern is counted independently (duplicates are counted separately).
        """
        count = 0
        for p in patterns:
            if p in word:
                count += 1
        return count
```
- Notes:
  - Approach: For each pattern, use Python's substring membership (`in`) to check if it appears in word. This is simple and efficient for the given constraints.
  - Time complexity: Let P = number of patterns, W = len(word), and L_i = len(patterns[i]). Worst-case complexity is O(sum_i (W * L_i)) for naive substring checks; practically Python uses optimized methods and with constraints (<=100) this is fine. Alternatively, if we denote max pattern length as L_max, it's O(P * W * L_max) worst-case.
  - Space complexity: O(1) extra space (beyond input), or O(1) ignoring input storage. If using the alternative substring-set approach it would be O(W^2) space.
  - Implementation details: We count duplicates separately as required by the problem examples.