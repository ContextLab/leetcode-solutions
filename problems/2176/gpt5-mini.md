# [Problem 2176: Count Equal and Divisible Pairs in an Array](https://leetcode.com/problems/count-equal-and-divisible-pairs-in-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the number of pairs (i, j) with i < j, nums[i] == nums[j], and (i * j) % k == 0. The constraints are small (n <= 100), so a straightforward O(n^2) check of all pairs is easy and safe.  
I also notice we could group indices by value and only check pairs inside each group (which reduces constant factors). Another micro-optimization: for each value group, count indices by residue modulo k and use residue combinations to count pairs whose product is divisible by k. But given n is small, the simplest double loop is clear and robust.

## Refining the problem, round 2 thoughts
Edge cases:
- If no value repeats, answer is 0.
- If k == 1, every pair with equal values qualifies (because any product is divisible by 1).
- Indices start at 0; note that 0 multiplied by anything is 0 which is divisible by any k -> any pair involving index 0 and equal values is automatically valid.

Time/space considerations:
- Brute force double loop: time O(n^2), space O(1).
- Group-by-value then pair inside groups is effectively the same worst-case complexity but can be slightly faster in practice.
Given constraints, O(n^2) is perfectly acceptable and simplest.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countPairs(self, nums: List[int], k: int) -> int:
        n = len(nums)
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] == nums[j] and (i * j) % k == 0:
                    count += 1
        return count
```
- Notes:
  - Approach: Straightforward nested loops over all index pairs (i < j). For each pair check equality of values and divisibility condition on the product of indices.
  - Time complexity: O(n^2), where n = len(nums). With n <= 100 this is fine.
  - Space complexity: O(1) extra space (excluding input).