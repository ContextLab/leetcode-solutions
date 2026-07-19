# [Problem 1081: Smallest Subsequence of Distinct Characters](https://leetcode.com/problems/smallest-subsequence-of-distinct-characters/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I recognize this as the same core problem as "Remove Duplicate Letters" (LeetCode 316). The task is to produce a subsequence (so relative order preserved) containing each distinct character exactly once and be lexicographically smallest possible. 

My immediate thought: greedy + stack. Walk through the string and build the result step-by-step. For each character, if it is already chosen (in the stack/result), skip it. Otherwise, consider popping larger characters from the end of the current result if they appear later in the string again (so we can still include them later) and popping them would make the result lexicographically smaller. Keep a record of the last occurrence index of each character to know whether it's safe to pop a character (i.e., it appears again later). Use a visited set/array to avoid duplicates in the result.

This is the classic monotonic-stack greedy solution. There are other approaches (recursive selection of the smallest char such that all distinct chars are still present in the suffix), but the stack approach is efficient and straightforward.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- If a character already included, ignore further occurrences.
- Use last occurrence indices to decide whether popping is safe: we can pop a char if its last occurrence index is after the current index (so it will be available later).
- Characters are lowercase English letters, so visited/last occurrences can be arrays of size 26 if desired.
- Complexity: each character is pushed and popped at most once -> O(n) time; space is O(26 + result) = O(n) worst-case but effectively O(1) extra besides output.
- Alternative recursive solution exists but less efficient/clear than greedy stack for iterative implementation.

Now produce the final working implementation.

## Attempted solution(s)
```python
class Solution:
    def smallestSubsequence(self, s: str) -> str:
        # last occurrence index for each character
        last = {c: i for i, c in enumerate(s)}
        stack = []
        in_stack = set()
        
        for i, c in enumerate(s):
            if c in in_stack:
                continue
            # While stack not empty and top char > current char and
            # top char appears later again (so we can pop it and re-add later)
            while stack and stack[-1] > c and last[stack[-1]] > i:
                removed = stack.pop()
                in_stack.remove(removed)
            stack.append(c)
            in_stack.add(c)
        
        return ''.join(stack)
```
- Notes on approach:
  - We compute last occurrence of each character to know if it's safe to remove a previously chosen character (we can re-add it later).
  - We maintain a stack (list) for the current subsequence and a set in_stack to track which characters are already included.
  - For each character c in the string (left to right):
    - If c already in result (in_stack), skip it.
    - Otherwise, while the stack's last character is lexicographically larger than c and that last character appears later in the string (last[...] > current index), pop it from stack and mark it as not in_stack. This makes the sequence lexicographically smaller.
    - Push current character and mark it as in_stack.
  - Return the joined stack as the result.

- Complexity:
  - Time: O(n), each character is pushed and popped at most once.
  - Space: O(n) for the output; extra space O(1) (bounded by alphabet size) for last and in_stack.