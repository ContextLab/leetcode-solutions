# [Problem 2375: Construct Smallest Number From DI String](https://leetcode.com/problems/construct-smallest-number-from-di_string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I want the lexicographically smallest string of digits 1..9 (no repeats) that satisfies the pattern of I (increasing) and D (decreasing). The pattern length is n so the result has length n+1 and digits 1..n+1 suffice (since n <= 8). Brute force by generating permutations is possible for n <= 8 but unnecessary and inefficient in principle. 

To get the smallest lexicographic number, we should choose the smallest available digit as early as possible while respecting future constraints. When we see a run of consecutive 'D's, the earliest positions in that run may need to be larger than later ones to satisfy descents; that suggests delaying assignment until the full D-run length is known. A stack-based or greedy approach that delays flushing digits until we see an 'I' (or the end) seems familiar and promising.

## Refining the problem, round 2 thoughts
Refinement: iterate positions 0..n. At each step push the next smallest unused digit (1..n+1) to a stack. When the next relation requires an increase (pattern[i] == 'I') or we've reached the end, flush the stack by popping all elements to the result. Popping produces a descending sequence which exactly handles prior 'D's; when we flush because of 'I', we make the earliest position as small as possible.

Edge cases: pattern all 'I' (we should get "123..."), pattern all 'D' (we should get the reverse "n+1...1"). This method covers both. Time complexity linear O(n), space O(n). Alternative is backtracking/permutations (exponential) — not needed.

## Attempted solution(s)
```python
class Solution:
    def smallestNumber(self, pattern: str) -> str:
        """
        Greedy + stack approach:
        Push increasing digits 1..n+1 onto a stack. Whenever we see an 'I' (or reach the end),
        pop all from the stack to output, which produces the correct descending sequences
        for previous 'D's and yields the lexicographically smallest result.
        """
        n = len(pattern)
        stack = []
        result = []

        # We need n+1 digits: 1 .. n+1
        for i in range(n + 1):
            # push next smallest digit
            stack.append(str(i + 1))
            # if at end or next relation is 'I', flush stack
            if i == n or pattern[i] == 'I':
                while stack:
                    result.append(stack.pop())

        return ''.join(result)
```
- Notes:
  - Approach: Greedy using a stack. Pushing successive numbers and popping when an 'I' or the end is encountered produces necessary descending runs for sequences of 'D' and keeps digits as small as possible early, guaranteeing lexicographically smallest result.
  - Time complexity: O(n), where n = len(pattern). Each of the n+1 digits is pushed once and popped once.
  - Space complexity: O(n) for the stack and result (both O(n+1) in practice).