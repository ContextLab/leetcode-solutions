# [Problem 1877: Minimize Maximum Pair Sum in Array](https://leetcode.com/problems/minimize-maximum-pair-sum-in-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to pair up all elements (n is even) so that the largest sum among the pairs is as small as possible. My first intuition: to avoid a very large pair sum, avoid pairing large numbers together. That suggests pairing large elements with small elements. If I sort the array, pairing the smallest with the largest seems natural. For a sorted array a0 <= a1 <= ... <= a_{n-1}, pairing a0 with a_{n-1}, a1 with a_{n-2}, etc., will balance sums. I should check if any counterexample exists to break that greedy approach. Also consider trivial case n=2: just sum of two elements.

## Refining the problem, round 2 thoughts
Greedy pairing (smallest with largest) is a common strategy for minimizing the maximum pair sum — it balances extremes. Intuitively, any other pairing that puts two large numbers together can only increase the maximum pair sum. A short informal proof: after sorting, for any pairing that doesn't match these extremes, you can swap to match extremes and not increase the maximum pair sum. So the two-pointer approach on the sorted array is correct.

Edge cases: n is guaranteed even, values are positive within [1, 1e5], so no worries about negatives or zero. Complexity: sorting dominates with O(n log n). Because max value is bounded, a counting-sort style solution (O(n + U)) is also possible, but sorting is simpler and fast enough for constraints (n up to 1e5).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minPairSum(self, nums: List[int]) -> int:
        """
        Sort the array and pair smallest with largest, second smallest with second largest, etc.
        Track the maximum pair sum encountered and return it.
        """
        nums.sort()
        n = len(nums)
        max_pair = 0
        i, j = 0, n - 1
        while i < j:
            pair_sum = nums[i] + nums[j]
            if pair_sum > max_pair:
                max_pair = pair_sum
            i += 1
            j -= 1
        return max_pair
```
- Notes:
  - Approach: Sort then use two pointers to pair smallest with largest. The answer is the maximum of these pair sums.
  - Time complexity: O(n log n) due to sorting.
  - Space complexity: O(1) extra space (or O(n) if counting the sort's auxiliary space), excluding the input storage and the sort's internal memory. An alternative counting-sort approach could achieve O(n + U) time where U = 10^5 (value range).