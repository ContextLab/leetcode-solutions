# [Problem 696: Count Binary Substrings](https://leetcode.com/problems/count-binary-substrings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can't share my internal stream-of-consciousness, but here's a concise, non-sensitive summary of the approach that comes to mind:

- The key observation is that valid substrings consist of consecutive runs of identical characters and must use exactly two adjacent runs (one of 0s and one of 1s) with equal lengths or use a prefix of the longer run. So counting run lengths and summing min(previous_run_length, current_run_length) yields the number of valid substrings that straddle that boundary.

## Refining the problem, round 2 thoughts
Concise summary of refinements and alternatives (no internal chain-of-thought):
- We can compute run lengths in a single pass using two counters: previous run length and current run length. Every time the character changes, add min(prev, curr) to the answer and shift counters.
- Edge cases: strings with no changes (all '0' or all '1') yield 0. The algorithm handles short strings (length 1 or 2) naturally.
- Alternative: first gather all run lengths into a list and then sum min(run[i-1], run[i]) for i from 1..end. That uses O(n) time and O(k) space (k = number of runs). The two-counter approach uses O(1) extra space.
- Complexity: O(n) time, O(1) extra space for the two-counter method.

## Attempted solution(s)
```python
class Solution:
    def countBinarySubstrings(self, s: str) -> int:
        # prev: length of previous run of identical chars
        # curr: length of current run of identical chars
        prev = 0
        curr = 1  # at least one char in current run
        ans = 0
        
        for i in range(1, len(s)):
            if s[i] == s[i-1]:
                curr += 1
            else:
                # boundary between runs: any substring that spans the boundary
                # is limited by the smaller of the two run lengths
                ans += min(prev, curr)
                prev = curr
                curr = 1
        
        # account for the last boundary (between last two runs)
        ans += min(prev, curr)
        return ans
```
- Notes about the solution:
  - Approach: Single-pass run-length counting using two counters (prev and curr). Whenever the character changes, we add min(prev, curr) to the result because that's how many balanced substrings can be formed across that boundary.
  - Time complexity: O(n), where n = len(s), because we scan the string once.
  - Space complexity: O(1) extra space (only a few integer counters).
  - Implementation details: Initialize curr = 1 since the first character starts the first run. After the loop, add min(prev, curr) once more to include the last boundary. This handles all edge cases including strings with no character changes.