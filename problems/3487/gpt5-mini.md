# [Problem 3487: Maximum Unique Subarray Sum After Deletion](https://leetcode.com/problems/maximum-unique-subarray-sum-after-deletion/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
At first glance this looks like the "maximum sum subarray with all unique elements" which usually suggests a sliding-window / two-pointer approach (Maximum Erasure Value). But the problem allows deleting any number of elements from the array first, then choosing a contiguous subarray of the resulting array. If I can delete arbitrary elements, I can make any chosen subsequence of the original array contiguous by deleting everything else. That means I'm effectively allowed to choose any subsequence (non-empty) of the original array whose values are pairwise distinct.

Given that interpretation, duplicates only matter by value (you can pick at most one occurrence of each value). To maximize sum of a set of unique values, I'd include every value that increases the total — i.e., include all positive distinct values. Zeros don't help but are harmless, negatives reduce the sum and so should be omitted unless forced to pick something non-empty. So the optimal answer should be the sum of all distinct positive numbers, except when there are no positive numbers (or no non-negative), in which case we must pick the largest element (the best single choice).

## Refining the problem, round 2 thoughts
- A sliding-window approach is unnecessary once we realize deletions let us pick any subsequence.
- Implementation: gather the set of distinct values and sum the positives.
- Edge cases:
  - If there are no positive distinct values, we still must pick a non-empty subsequence: choose the maximum element in nums (could be 0 or a negative).
  - Duplicates of a positive value don't allow adding it multiple times — we sum each distinct value at most once.
- Complexity: collecting distinct values is O(n) time and O(U) space (U ≤ 201 because values in [-100,100], but even general distinct ≤ n). This is optimal.

## Attempted solution(s)
```python
class Solution:
    def maximumUniqueSubarray(self, nums: list[int]) -> int:
        # Sum of all distinct positive values
        distinct = set(nums)
        sum_positive_distinct = sum(x for x in distinct if x > 0)
        # We must return a non-empty subarray sum; if there are no positive distinct values,
        # return the maximum element (could be 0 or a negative).
        return max(sum_positive_distinct, max(nums))
```
- Notes:
  - Approach: Use the fact that arbitrary deletions let us pick any subsequence; uniqueness is by value, so include each positive value at most once. If no positives, pick the largest element to satisfy non-empty constraint.
  - Time complexity: O(n) to scan nums and build the set.
  - Space complexity: O(min(n, range_of_values)) for the set of distinct values.