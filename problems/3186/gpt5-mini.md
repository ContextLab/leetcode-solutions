# [Problem 3186: Maximum Total Damage With Spell Casting](https://leetcode.com/problems/maximum-total-damage-with-spell-casting/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given spells with integer damages and a constraint: if we pick damage value x, we cannot pick any spells with damage x-2, x-1, x+1, or x+2. Multiple spells can have the same damage but each instance can be used once. This reminds me of "Delete and Earn" (or weighted house robber) where grouping equal values and treating each distinct value as a weighted node is useful. Here, picking a value x excludes values within distance 2 (i.e., values x-2..x+2), so chosen values must be separated by at least 3. So compress identical values by summing total damage for that value (weight = value * count). Then we have distinct values on the integer line; we want to pick a subset of these weighted points, no two within distance <=2, to maximize total weight. That becomes a weighted interval scheduling or DP on sorted distinct values.

A straightforward DP: sort unique values vals[], for each index i compute dp[i] = max(dp[i-1], weight[i] + dp[j]) where j is the last index with vals[j] <= vals[i] - 3 (the last non-conflicting value). We can find j with binary search (bisect) on vals.

## Refining the problem, round 2 thoughts
Edge cases:
- All values equal — then either take all (since same value conflicts only with ±1/±2 but same value is allowed to aggregate) — our grouping handles that.
- Sparse values — binary search handles large gaps naturally.
- Very large values up to 1e9 — we must not create large arrays indexed by value; sorting unique values is fine (unique count <= 1e5).
Complexity:
- Counting frequencies: O(n)
- Sorting unique values: O(m log m) where m is number of distinct values (<= n)
- For each of m values, a binary search O(log m), so O(m log m) for DP. Total O(n + m log m).
We could implement a two-pointer walk to compute j in O(m), making total O(n + m), but O(m log m) is fine for constraints.

## Attempted solution(s)
```python
from typing import List
from collections import Counter
import bisect

class Solution:
    def maximumTotalDamage(self, power: List[int]) -> int:
        # Count total damage per distinct value
        cnt = Counter(power)
        vals = sorted(cnt.keys())
        weights = [v * cnt[v] for v in vals]
        
        m = len(vals)
        if m == 0:
            return 0
        
        dp = [0] * m
        for i in range(m):
            w = weights[i]
            # find last index j where vals[j] <= vals[i] - 3
            target = vals[i] - 3
            j = bisect.bisect_right(vals, target) - 1
            take = w + (dp[j] if j >= 0 else 0)
            not_take = dp[i-1] if i > 0 else 0
            dp[i] = max(not_take, take)
        
        return dp[-1]
```
- Notes about approach:
  - We group equal damage values and treat each distinct damage as an item with weight = value * count.
  - Sorting distinct values lets us do DP where picking a value excludes any value within ±2, so we only add the best non-conflicting dp[j] where vals[j] <= vals[i] - 3.
- Complexity:
  - Time: O(n + m log m) where n = len(power) and m = number of distinct damage values (m <= n). Counting is O(n), sorting O(m log m), DP with binary search O(m log m).
  - Space: O(m) for arrays cnt/vals/weights/dp.