# [Problem 3583: Count Special Triplets](https://leetcode.com/problems/count-special-triplets/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need triplets (i, j, k) with i < j < k and nums[i] == nums[j]*2 and nums[k] == nums[j]*2. That means for any chosen center j, we are looking for equal values "need = 2 * nums[j]" both to the left and to the right of j. A brute-force triple loop is O(n^3) and impossible for n up to 1e5. For each j we just need the count of "need" on the left and the count on the right; multiply them to get the number of triplets using that j. So maintain counts of values to the left and right while scanning j from left to right. This suggests an O(n) single-pass approach using frequency maps.

## Refining the problem, round 2 thoughts
Implementation detail: initialize right-count as frequency of all numbers; left-count empty. For each index j in order:
- decrement right-count for nums[j] (since j is not part of right-side anymore),
- compute need = nums[j] * 2,
- contribution = left_count[need] * right_count[need],
- add contribution to answer,
- increment left-count[nums[j]].

Edge cases: nums[j] can be 0 (then need=0) — the formula still works. need might exceed the original value range (up to 2*10^5), so use a dict/Counter (or array with size >= 2*max(nums)+1) to be safe. Use modulo 1e9+7 for the running total. Complexity: O(n) time, O(M) space where M is number of distinct values (or up to max value range).

## Attempted solution(s)
```python
from collections import Counter

class Solution:
    def countTriplets(self, nums: list[int]) -> int:
        MOD = 10**9 + 7
        right = Counter(nums)  # counts of values to the right (initially whole array)
        left = Counter()       # counts of values to the left (initially empty)
        ans = 0

        for val in nums:
            # this index j is being considered as the middle element
            # remove it from right (so right now represents indices > j)
            right[val] -= 1
            if right[val] == 0:
                # optional cleanup to keep Counter small
                del right[val]

            need = val * 2
            # number of choices for i is left[need], for k is right[need]
            ans = (ans + left.get(need, 0) * right.get(need, 0)) % MOD

            # include current val in left for future js
            left[val] += 1

        return ans
```
- Notes:
  - Approach: single pass over the array using two frequency counters (left and right). For each center j, multiply the counts of 2*nums[j] on the left and right to get the number of valid (i,k) pairs for that j.
  - Time complexity: O(n), where n = len(nums). Each element processed once and dictionary operations are average O(1).
  - Space complexity: O(M) for the counters, where M is the number of distinct values (or up to the value range, at most about 2 * max(nums) + 1 if using arrays).
  - Handles zeros and large values safely by using Counters; intermediate results are taken modulo 1e9+7.