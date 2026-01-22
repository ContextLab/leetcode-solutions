# [Problem 2696: Minimum String Length After Removing Substrings](https://leetcode.com/problems/minimum-string-length-after-removing-substrings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to repeatedly remove occurrences of "AB" or "CD" until none remain and return the final length. My first thought is to simulate removals. A naive approach would repeatedly search for "AB" or "CD" and remove them (e.g., using string replace in a loop), but that can be inefficient and tricky about termination ordering.

This looks like the common pattern where local adjacent cancellations occur (pairs "AB" and "CD" cancel). That suggests using a stack: iterate left to right, push characters, and whenever the top of the stack plus current character form "AB" or "CD", pop the stack instead of pushing the current character (simulating removing that substring). This is linear time and straightforward.

## Refining the problem, round 2 thoughts
- Correctness: removing an adjacent pair only ever helps (reduces length by 2), and the stack simulation performs all possible cancellations that can arise (including new ones formed after removals), so it yields the minimal possible length.
- Edge cases: strings with no removable pairs remain unchanged; overlapping pairs such as "ABAB" are handled correctly by the stack (first AB removed, then the second).
- Alternatives: repeated replace/regex until no change (simpler to write but potentially O(n^2)); dynamic programming is unnecessary here.
- Complexity: single pass over string O(n) time, O(n) extra space for the stack worst-case. Input bounds are small (n <= 100), so either approach would pass, but stack is optimal and clear.

## Attempted solution(s)
```python
class Solution:
    def minimumLength(self, s: str) -> int:
        stack = []
        for ch in s:
            if stack:
                top = stack[-1]
                # If the top + current form a removable pair, pop instead of pushing
                if (top == 'A' and ch == 'B') or (top == 'C' and ch == 'D'):
                    stack.pop()
                    continue
            stack.append(ch)
        return len(stack)
```
- Notes:
  - Approach: use a stack to simulate removing "AB" and "CD" whenever they appear. When current char together with stack top form a removable pair, pop the stack and do not push the current char (effectively removing that substring). Otherwise push the current char.
  - Time complexity: O(n), where n = len(s), because each character is pushed/popped at most once.
  - Space complexity: O(n) worst-case for the stack.
  - Implementation details: checking only the two allowed removal pairs keeps the logic simple and efficient.