# [Problem 2200: Find All K-Distant Indices in an Array](https://leetcode.com/problems/find-all-k-distant-indices-in-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need all indices i for which there exists a j with nums[j] == key and |i - j| <= k. The straightforward idea is: find every position j where nums[j] == key, then mark the interval [j-k, j+k] (clamped to array bounds) as "covered". Finally collect all indices that are covered. Naively marking each interval by setting booleans is simple and fine for n up to 1000. Another slightly more optimal approach is to use a difference array (range increment via two endpoints) and then prefix-sum to get coverage counts — this avoids repeated writes when many keys overlap.

## Refining the problem, round 2 thoughts
Edge cases:
- k could be >= n, so a single key would cover the whole array (clamp bounds).
- If there are multiple key positions, intervals can overlap — that's fine; we only need to know if coverage > 0.
Time/space:
- Naive marking by setting booleans for each key interval is O(n * m) worst-case where m is count of keys (worst O(n^2) but n <= 1000).
- Difference-array approach is O(n + m) time and O(n) space and is easy to implement.
I'll implement the difference-array solution for clarity and efficiency.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findKDistantIndices(self, nums: List[int], key: int, k: int) -> List[int]:
        n = len(nums)
        # difference array of length n+1 to allow r+1 decrement
        diff = [0] * (n + 1)
        
        # For every index j where nums[j] == key, add +1 to diff[l], -1 to diff[r+1]
        for j, val in enumerate(nums):
            if val == key:
                l = max(0, j - k)
                r = min(n - 1, j + k)
                diff[l] += 1
                diff[r + 1] -= 1
        
        # Build prefix sums to see which indices are covered (>0)
        res = []
        curr = 0
        for i in range(n):
            curr += diff[i]
            if curr > 0:
                res.append(i)
        return res
```
- Approach: Use a difference array to mark intervals [j-k, j+k] for each position j where nums[j] == key. Prefix-sum the difference array to get coverage counts; any index with count > 0 is k-distant.
- Time complexity: O(n + m) where m is number of key occurrences (actually O(n + number_of_keys)). In practice this is O(n).
- Space complexity: O(n) for the difference array and output.
- Implementation details: clamped interval endpoints l and r ensure we don't go out of bounds; diff has length n+1 so r+1 is always valid. The result is naturally in increasing order because we iterate indices from 0 to n-1.