# [Problem 3174: Clear Digits](https://leetcode.com/problems/clear-digits/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see we repeatedly delete the first digit and the closest non-digit character to its left. That suggests a left-to-right process: whenever a digit is encountered, it will be paired with some previous letter (the closest non-digit to its left). This pairing is exactly what a stack models: push letters, and when a digit arrives pop one letter (and drop the digit). There's no reason to simulate deletions across the whole string repeatedly; a single pass suffices. Edge cases: if the string starts with digits that have no letter to their left — but the problem guarantees it's possible to delete all digits, so we won't encounter an unmatched digit in a correct input.

## Refining the problem, round 2 thoughts
So algorithm: iterate characters left-to-right; if char is a letter, push to stack; if char is a digit, pop one letter from the stack (if any). At the end the stack contains remaining letters in order. Complexity is O(n) time and O(n) extra space in worst case. We should guard the pop with a check, though constraints say inputs are valid. Example "cb34": c b => stack ['c','b'], see '3' pop 'b' -> ['c'], see '4' pop 'c' -> []. Works. If no digits, we just return original string.

## Attempted solution(s)
```python
class Solution:
    def clearDigits(self, s: str) -> str:
        """
        Use a stack: push non-digit characters; when encountering a digit,
        pop the closest non-digit to its left (if any). Return the remaining characters.
        """
        stack = []
        for ch in s:
            if ch.isdigit():
                # Problem guarantees it's possible to delete all digits,
                # but be safe and check before popping.
                if stack:
                    stack.pop()
            else:
                stack.append(ch)
        return ''.join(stack)
```
- Notes:
  - Approach: single-pass stack simulation of the leftward pairing of digits with the nearest non-digit to the left.
  - Time complexity: O(n), where n = len(s), since each character is processed once and each letter is pushed/popped at most once.
  - Space complexity: O(n) worst-case for the stack (when there are no digits).
  - Implementation detail: ch.isdigit() detects digits; else treat as non-digit (lowercase letters per constraints). The pop is guarded though per constraints it should always be valid.