# [Problem 796: Rotate String](https://leetcode.com/problems/rotate-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share my internal stream-of-consciousness. Brief summary instead: check whether goal is a rotation of s. Observations that lead to a simple solution: rotations of s are exactly the substrings of s+s with length len(s). So verify lengths match and test whether goal is contained in s+s. A fallback method is to check all n rotations explicitly.

## Refining the problem, round 2 thoughts
- Must first ensure s and goal have equal length; if not, return False.
- If lengths match, there are two simple approaches:
  1. Concatenate s with itself and check whether goal is a substring of s+s (very concise).
  2. Iterate through all possible rotations (0..n-1) and compare s rotated to goal.
- Complexity:
  - Using substring check: creating s+s is O(n) space and using Python's substring search is typically efficient; worst-case time is O(n^2) for naive comparisons, though implementations often use optimized algorithms.
  - Explicit rotation checks are O(n^2) time and O(1) extra space.
  - For guaranteed linear time, one could use KMP on s+s to search for goal in O(n), but given constraints (n <= 100) the substring approach is fully adequate.
- Edge cases: empty strings (not present due to constraints), single-character strings, identical strings, and completely different strings.

## Attempted solution(s)
```python
class Solution:
    def rotateString(self, s: str, goal: str) -> bool:
        # If lengths differ, rotation is impossible
        if len(s) != len(goal):
            return False
        # Quick check: if equal, goal must be substring of s+s
        return goal in (s + s)
```
- Notes:
  - Approach: check length equality, then test membership of goal in s+s.
  - Time complexity: O(n^2) in the worst case for substring search with naive comparisons; practically efficient for n <= 100. Using KMP would reduce to O(n) time.
  - Space complexity: O(n) due to creating s+s.