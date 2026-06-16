# [Problem 3612: Process String with Special Operations I](https://leetcode.com/problems/process-string-with-special-operations-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t provide internal stream-of-consciousness, but here is a concise summary of the intended approach:
- Simulate processing the input string s from left to right.
- Maintain the current result as a list of characters for efficient append/pop/extend/reverse.
- For letters: append; for '*': pop if non-empty; for '#': duplicate current list (extend with a copy); for '%': reverse the list.
- Finally join the list into a string and return.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- When '*' appears while result is empty, do nothing.
- When '#' appears on an empty result, result remains empty.
- Use a list of characters rather than repeated string concatenation to avoid quadratic string operations.
- Be careful when duplicating: extend with a snapshot copy (res.copy() or res[:]) to avoid in-place iteration issues.
- Complexity: result can grow exponentially if many '#' operators appear. Given s.length <= 20, the final length is bounded (worst-case doubling each time but still manageable). Time is proportional to the total work done to build/manipulate the result (sum of lengths produced/modified), and space is proportional to the final result length.

## Attempted solution(s)
```python
class Solution:
    def processString(self, s: str) -> str:
        res = []
        for ch in s:
            if ch == '*':
                if res:
                    res.pop()
            elif ch == '#':
                # duplicate current result: extend with a snapshot copy
                res.extend(res.copy())
            elif ch == '%':
                # reverse in place
                res.reverse()
            else:
                # lowercase letter
                res.append(ch)
        return ''.join(res)
```
- Notes:
  - Approach: direct simulation using a list of characters for O(1) append/pop and O(n) for duplicate/reverse where n is current result length.
  - Time complexity: O(M) where M is the total amount of work performed on the result across all operations (in the worst case this can be up to the final result length which may grow exponentially with the number of '#' operators). Given constraint s.length <= 20, this is practically bounded.
  - Space complexity: O(L) where L is the final result length.