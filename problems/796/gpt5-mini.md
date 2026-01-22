# [Problem 796: Rotate String](https://leetcode.com/problems/rotate-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share internal stream-of-consciousness, but here is a concise summary of the approach: Check trivial constraints (length equality). A well-known observation is that every rotation of s is a substring of s + s. So if goal is a rotation of s, goal must appear in s + s. This yields a very simple check.

## Refining the problem, round 2 thoughts
I won’t provide inner monologue, but a short clarification and alternatives:
- Verify lengths first; if lengths differ, immediately return False.
- Primary approach: return goal in (s + s).
- Alternative approaches: simulate k shifts (O(n^2) worst-case) or use a string-search algorithm (KMP) to get guaranteed O(n) time for the substring check.
- Edge cases: identical strings, minimal length strings. Constraints ensure lengths are between 1 and 100, and characters are lowercase letters.

## Attempted solution(s)
```python
class Solution:
    def rotateString(self, s: str, goal: str) -> bool:
        # If lengths differ, s cannot be rotated to goal.
        if len(s) != len(goal):
            return False
        # All rotations of s are substrings of s + s.
        return goal in (s + s)
```
- Notes:
  - Approach: Check length equality, then test whether goal is a substring of s + s.
  - Time complexity: O(n^2) worst-case if using a naive substring search; in practice Python's substring search is highly optimized and often behaves close to O(n). With KMP it could be made worst-case O(n). Here n = len(s).
  - Space complexity: O(n) extra for constructing s + s.