# [Problem 1760: Minimum Limit of Balls in a Bag](https://leetcode.com/problems/minimum-limit-of-balls-in-a-bag/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to minimize the maximum number of balls in any bag after at most maxOperations splits. Splitting reduces large numbers into smaller pieces. This feels like a decision/search problem: for a candidate penalty X, can we make every bag <= X with at most maxOperations splits? If we can, we might try a smaller X; if we cannot, we must increase X. That suggests binary search on the answer (the penalty). 

How to check feasibility for a given X? For a bag with value v, we need to split it into k pieces so that each piece <= X. Minimum k is ceil(v / X). Number of operations (splits) required = k - 1 = ceil(v/X) - 1. Summing those across nums gives total operations needed. If total <= maxOperations then X is feasible. The search range is [1, max(nums)].

A greedy approach of repeatedly splitting the largest bag (with a heap) also comes to mind, but that would be slower and tricky for large inputs. Binary search is straightforward and efficient.

## Refining the problem, round 2 thoughts
- Confirm formula: ceil(v/X)-1 equals (v-1)//X. So for each v we can compute ops_needed = (v-1)//X.
- Binary search bounds: low = 1, high = max(nums).
- Termination: typical while low < high pattern; compute mid; if operations_needed(mid) <= maxOperations then high = mid else low = mid + 1. Return low.
- Complexity: each check costs O(n) to sum ops; binary search over range up to max(nums) (<= 1e9) costs O(log max(nums)) iterations, so total O(n log max(nums)). Space O(1) extra.
- Edge cases: nums length up to 1e5 and values up to 1e9 — the algorithm handles that fine in Python. maxOperations can be very large but our arithmetic stays within Python integers.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumSize(self, nums: List[int], maxOperations: int) -> int:
        # Binary search on the penalty (maximum allowed balls in a bag)
        low, high = 1, max(nums)
        
        def ops_needed(limit: int) -> int:
            # For each bag of size v, need (v-1)//limit operations to make pieces <= limit
            total = 0
            for v in nums:
                total += (v - 1) // limit
                # Early exit if already exceed allowed operations
                if total > maxOperations:
                    return total
            return total
        
        while low < high:
            mid = (low + high) // 2
            if ops_needed(mid) <= maxOperations:
                high = mid
            else:
                low = mid + 1
        return low
```
- Notes:
  - Approach: Binary search the minimal possible penalty. For a candidate limit X, compute the minimum number of splits required by summing (v-1)//X for each v in nums. If the sum <= maxOperations, X is feasible.
  - Time complexity: O(n log M) where n = len(nums) and M = max(nums) (log M from binary search).
  - Space complexity: O(1) extra space (ignoring input storage).
  - Implementation detail: early exit in ops_needed when accumulated operations exceed maxOperations to save time on large inputs.