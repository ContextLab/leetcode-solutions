# [Problem 2554: Maximum Number of Integers to Choose From a Range I](https://leetcode.com/problems/maximum-number-of-integers-to-choose-from-a-range-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to choose as many distinct integers from [1..n] as possible, not using those in banned, and the total sum must not exceed maxSum. To maximize count with a sum constraint, a natural greedy idea is to take the smallest allowed numbers first (because smaller numbers give more items for the same sum). So iterate from 1 to n, skip banned numbers, and keep adding while the running sum <= maxSum. As soon as adding the next available integer would exceed maxSum we stop. Banned values can be put in a set for O(1) checks. Complexity should be O(n + len(banned)) time, O(len(banned)) space.

## Refining the problem, round 2 thoughts
- Confirm greedy correctness: picking the smallest available integers yields the maximum count because any other choice that includes a larger number instead of a smaller unused number can only reduce the possible count for the same sum budget.
- Edge cases: banned may contain numbers > n (we ignore them), maxSum may be very small (zero or 1) so we might pick none, or banned might block small numbers forcing us to pick slightly larger ones but greedy still holds.
- Implementation details: convert banned to a set, iterate i from 1..n inclusive, skip if banned, check if curr_sum + i <= maxSum then include, else break. This is efficient for given constraints.
- Complexity: time O(n + m) where m = len(banned), space O(m).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxCount(self, banned: List[int], n: int, maxSum: int) -> int:
        banned_set = set(banned)
        curr_sum = 0
        count = 0
        for x in range(1, n + 1):
            if x in banned_set:
                continue
            if curr_sum + x > maxSum:
                break
            curr_sum += x
            count += 1
        return count
```
- Notes:
  - Approach: Greedy — choose the smallest available integers from 1 to n that are not banned until the sum budget is exhausted.
  - Time complexity: O(n + m) where m = len(banned) (to build the set and iterate up to n).
  - Space complexity: O(m) for the banned set.
  - Implementation detail: Breaking early when the next number would exceed maxSum improves average runtime when maxSum is small.