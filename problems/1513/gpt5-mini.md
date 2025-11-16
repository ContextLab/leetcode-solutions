# [Problem 1513: Number of Substrings With Only 1s](https://leetcode.com/problems/number-of-substrings-with-only-1s/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share internal stream-of-consciousness. Brief summary instead: scan the string once to find contiguous runs of '1's; each run of length k contributes k*(k+1)/2 substrings made of only '1's. Sum those contributions modulo 10^9+7.

## Refining the problem, round 2 thoughts
- We need a single pass O(n) algorithm: iterate through s, count current consecutive '1's; when a '0' or end is reached, add k*(k+1)//2 to the result and reset the counter.
- Use modulo 1_000_000_007 to avoid overflow; apply modulo when adding each run's count.
- Edge cases: all zeros (answer 0), all ones (single run), alternating characters.
- Alternative: maintain running contribution incrementally (add current_count when you see a '1'), but both approaches are O(n) time and O(1) space.
- Time complexity: O(n). Space complexity: O(1).

## Attempted solution(s)
```python
class Solution:
    def numSub(self, s: str) -> int:
        MOD = 10**9 + 7
        res = 0
        count = 0  # current consecutive '1's
        
        for ch in s:
            if ch == '1':
                count += 1
            else:
                if count:
                    res = (res + count * (count + 1) // 2) % MOD
                    count = 0
        # handle trailing run of '1's
        if count:
            res = (res + count * (count + 1) // 2) % MOD
        
        return res
```
- Notes:
  - Approach: Count contiguous '1' runs. For a run of length k, number of substrings inside it = k*(k+1)/2 (sum of 1..k).
  - Time complexity: O(n), where n = len(s), because we scan the string once.
  - Space complexity: O(1), only a few integer variables used.
  - Implementation detail: use modulo 10^9+7 when adding each run to keep numbers small.