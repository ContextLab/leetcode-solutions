# [Problem 2615: Sum of Distances](https://leetcode.com/problems/sum-of-distances/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need for each index i the sum of absolute differences |i - j| for all other indices j that have the same value nums[j] == nums[i]. A brute-force approach would for each i scan all other indices with the same value and sum distances — but that could be O(k^2) for k occurrences of a value and overall O(n^2) worst-case, which is too slow for n up to 1e5.

Because distance uses indices and absolute differences, if we group indices of equal values and sort them (they're naturally in increasing order if we collect by scanning), there's structure: given positions p0 < p1 < ... < p(m-1), for position pk the sum of distances to all others can be computed using prefix sums of positions:
- sum_left = k * pk - sum(p0..p(k-1))
- sum_right = sum(p(k+1)..p(m-1)) - (m-1-k) * pk
Combine to get the answer for pk in O(1) after computing prefix sums for that group. So overall O(n) time.

## Refining the problem, round 2 thoughts
Implementation details:
- First pass: build a map from value -> list of indices (appending index in increasing order).
- For each list of indices of length m:
  - If m == 1, answer is 0.
  - Build prefix sums of indices (or maintain running sum).
  - For each position k compute left_count, right_count, left_sum, right_sum and apply formula.
Edge cases: single occurrences produce 0. Large input requires O(n) time and O(n) extra memory for groups and result array. Using integers only; sums fit within Python int.

Time complexity: O(n) overall (each index is added to a list once and processed once). Space complexity: O(n) for groups + O(n) output.

## Attempted solution(s)
```python
from collections import defaultdict
from typing import List

class Solution:
    def distance(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [0] * n
        groups = defaultdict(list)
        
        # collect indices for each value
        for i, v in enumerate(nums):
            groups[v].append(i)
        
        # process each group using prefix sums
        for indices in groups.values():
            m = len(indices)
            if m == 1:
                continue
            # build prefix sums of indices
            prefix = [0] * m
            prefix[0] = indices[0]
            for i in range(1, m):
                prefix[i] = prefix[i-1] + indices[i]
            total = prefix[-1]
            
            # compute result for each index in this group
            for k, idx in enumerate(indices):
                left_count = k
                right_count = m - 1 - k
                left_sum = prefix[k-1] if k > 0 else 0
                right_sum = total - prefix[k]
                res[idx] = idx * left_count - left_sum + right_sum - idx * right_count
        
        return res
```
- Notes:
  - Approach: group equal elements' indices, use prefix sums per group to compute sum of distances in O(1) per index.
  - Time complexity: O(n) — each index is appended and then processed once.
  - Space complexity: O(n) — storage for groups and result array.
  - Handles edge cases where a value appears only once (result remains 0).