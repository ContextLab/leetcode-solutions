# [Problem 2434: Using a Robot to Print the Lexicographically Smallest String](https://leetcode.com/problems/using-a-robot-to-print-the-lexicographically-smallest-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share my internal stream-of-consciousness. I can, however, give a concise high-level approach:

High-level approach summary: maintain a stack t for characters moved from s, and maintain counts of remaining characters in s. For each character moved from s to t, if the top of t is lexicographically <= the smallest character remaining in s, pop from t to the output. Continue until both s and t are empty. This yields the lexicographically smallest possible output.

## Refining the problem, round 2 thoughts
Refinements and considerations:
- Use a frequency array of size 26 to track remaining characters in s so we can quickly know the smallest remaining character.
- Use a list as a stack for t and a list for the output p (then join).
- For each character c in s (processed left to right):
  - Decrement its count in the frequency array and push c onto the stack.
  - While the stack is non-empty and stack[-1] <= smallest remaining char in s (found by advancing a pointer over the frequency array), pop stack to output.
- After processing all characters from s, pop any remaining characters from the stack to the output.
Edge cases:
- All characters same — result is same characters.
- Already sorted characters — can frequently pop while processing.
Time complexity: O(n) since each character is pushed/popped at most once and the smallest-char pointer advances at most 26 steps in total.
Space complexity: O(n) for the stack and output.

## Attempted solution(s)
```python
class Solution:
    def robotWithString(self, s: str) -> str:
        # Frequency of remaining characters in s
        freq = [0] * 26
        for ch in s:
            freq[ord(ch) - ord('a')] += 1

        # pointer to smallest remaining character (0..25)
        min_c = 0
        while min_c < 26 and freq[min_c] == 0:
            min_c += 1

        stack = []
        res = []

        for ch in s:
            idx = ord(ch) - ord('a')
            # consume this char from remaining s
            freq[idx] -= 1
            # update smallest remaining char pointer
            while min_c < 26 and freq[min_c] == 0:
                min_c += 1

            # push to t (stack)
            stack.append(ch)

            # pop from stack to result while top <= smallest remaining char
            # if no remaining chars, min_c will be 26, so condition becomes True for any char
            while stack and (min_c == 26 or stack[-1] <= chr(min_c + ord('a'))):
                res.append(stack.pop())

        # pop any remaining in stack
        while stack:
            res.append(stack.pop())

        return ''.join(res)
```
- Notes about the solution:
  - Correctness: At each step, we only write (pop from t to paper) when it is safe to do so without preventing a lexicographically smaller result — i.e., when the top of t is <= any character that could still be moved from s later.
  - Time complexity: O(n) where n = len(s). Each character is pushed and popped at most once. The min-char pointer advances at most 26 times overall.
  - Space complexity: O(n) for the stack and output.