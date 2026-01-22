# [Problem 2560: House Robber IV](https://leetcode.com/problems/house-robber-iv/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to choose at least k non-adjacent houses so that the maximum value among chosen houses (the robber's "capability") is as small as possible. That suggests we want a threshold t (capability) and check whether it's possible to pick >= k houses all with value <= t and still respect the non-adjacent constraint. If we can check feasibility for a given t, we can binary-search the minimal t.

How to check for a given t? Consider marking houses with nums[i] <= t as "available". We want the maximum number of non-adjacent available houses. A greedy scan works: whenever we encounter an available house, take it and skip the next house (to maintain non-adjacency). That gives the maximum count because taking the earliest available house can't hurt the ability to take later ones (classic interval/packing greedy). If count >= k then t is feasible.

Binary search bounds can be from min(nums) to max(nums) (or 1..1e9). Complexity will be O(n log V).

Edge cases: k >= 1 always, length up to 1e5 so O(n log V) is fine. Also ensure correctness when consecutive unavailable houses exist.

## Refining the problem, round 2 thoughts
- The check function should be O(n) and simple: iterate i from 0 to n-1, if nums[i] <= t then take it (count++), i += 2 else i += 1.
- We could binary-search only on sorted unique values of nums, reducing iterations, but standard binary search on numeric range (min..max) is simpler and fast enough (log2(1e9) ~ 30).
- Alternative: dynamic programming to compute maximum picks for each t is overkill; greedy suffices for the 1D non-adjacent picking.
- Confirm monotonicity: if t works, any t' >= t also works (more houses become available), so binary search is valid.
- Complexity: O(n log V) time, O(1) extra space.
- Ensure to handle large values (ints) and typical Python speed; using direct while loop is fine.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minCapability(self, nums: List[int], k: int) -> int:
        n = len(nums)
        lo, hi = min(nums), max(nums)

        def can(cap: int) -> bool:
            # Greedy: take an available house (nums[i] <= cap) and skip next
            count = 0
            i = 0
            while i < n:
                if nums[i] <= cap:
                    count += 1
                    i += 2
                else:
                    i += 1
                if count >= k:
                    return True
            return False

        ans = hi
        while lo <= hi:
            mid = (lo + hi) // 2
            if can(mid):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        return ans
```
- Notes:
  - Approach: binary search the minimal capability cap. For each cap, greedily count how many non-adjacent houses with value <= cap can be taken. If the count >= k, cap is feasible.
  - Time complexity: O(n * log V) where V = max(nums) - min(nums) (or effectively log(max(nums))) — at most ~30 iterations for 32-bit ints, so overall O(n log 1e9) which is fine for n up to 1e5.
  - Space complexity: O(1) additional space (ignoring input).