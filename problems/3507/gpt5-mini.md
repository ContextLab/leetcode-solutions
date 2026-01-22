# [Problem 3507: Minimum Pair Removal to Sort Array I](https://leetcode.com/problems/minimum-pair-removal-to-sort-array-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given a deterministic operation: repeatedly pick the adjacent pair with the minimum sum (leftmost if tie), replace the pair by their sum (so the array shortens by one). We need the minimum number of such operations to make the array non-decreasing. Because the operation choice is fixed by the problem statement (minimum-sum adjacent pair, leftmost tie), there is no branching: the sequence of merges is deterministic. Therefore we can simulate the process step by step until the array becomes non-decreasing (or reduces to length 1). Constraints are small (n <= 50), so a straightforward simulation scanning for the minimum pair each time is cheap. Watch for negative numbers and tie-breaking (leftmost): implement the min-sum search to only update on strictly smaller sums so ties keep the earlier index.

## Refining the problem, round 2 thoughts
Edge cases:
- Already non-decreasing: answer 0.
- Single element (though constraint says n >= 1): already non-decreasing, answer 0.
- All negatives: still works—minimum sum is most negative, leftmost tie must be honored.
Because n is small, an O(n^2) simulation is fine (at most n-1 merges, each scan for min pair takes O(n)). Alternatively a heap with lazy updates is overkill here. Implementation detail: after merging at index i, replace nums[i] with sum and remove nums[i+1]. Re-check non-decreasing property each iteration. Count operations until sorted. Time complexity O(n^2), space O(1) additional.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        # Helper to check non-decreasing
        def is_non_decreasing(arr: List[int]) -> bool:
            return all(arr[i] >= arr[i-1] for i in range(1, len(arr)))
        
        ops = 0
        # If already non-decreasing, return 0
        if is_non_decreasing(nums):
            return 0
        
        # Simulate until array becomes non-decreasing
        while len(nums) > 1 and not is_non_decreasing(nums):
            min_sum = float('inf')
            min_idx = 0
            # find leftmost adjacent pair with minimum sum
            for i in range(len(nums) - 1):
                s = nums[i] + nums[i + 1]
                if s < min_sum:
                    min_sum = s
                    min_idx = i
            # merge the pair at min_idx
            nums[min_idx] = min_sum
            del nums[min_idx + 1]
            ops += 1
        
        return ops
```
- Notes:
  - Approach: direct simulation of the deterministic process: find the leftmost adjacent pair with the minimum sum, replace it by their sum, repeat until the array is non-decreasing.
  - Time complexity: O(n^2) worst-case (at most n-1 merges, each scanning O(n) to find the minimum pair and O(n) check for non-decreasing). With n <= 50 this is easily acceptable.
  - Space complexity: O(1) extra (modifies the input list in-place; aside from that uses constant extra space).
  - Implementation details: tie-breaking (leftmost) is naturally handled by updating min only on strictly smaller sums. The non-decreasing check uses a simple linear scan.