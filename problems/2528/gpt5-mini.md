# [Problem 2528: Maximize the Minimum Powered City](https://leetcode.com/problems/maximize-the-minimum-powered-city/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to maximize the minimum "power" across all cities after adding up to k stations. Each station contributes to a contiguous window of length 2*r+1 around its position. The problem smells like a binary-search-on-answer: for a candidate minimum power X, check if we can, with ≤ k added stations, make every city's power at least X.

To check feasibility for X we need to know each city's current power from existing stations (a sliding window sum). Then we must decide where to place additional stations greedily so each city meets X. A common greedy: sweep left-to-right, keep track of extra contribution from stations we already placed (use a difference array to expire contributions), and when the current city is under X, place enough stations at the rightmost position that still covers this city (i + r, capped by n-1). Placing them as far right as possible maximizes their future effect. Update the diff/ending index so recorded extra contributions expire appropriately.

So plan:
- Compute base power for each city via prefix sums (sliding window).
- Binary search answer in [0, sum(stations) + k].
- For each mid, simulate greedy check with diff array in O(n).

Careful with indices for "expiry" of added station contributions: if we place at pos = min(n-1, i + r), a station there covers cities from pos - r to pos + r. When pos = i + r (the common case), the coverage on the sweep starting at i is from i to i + 2r, so expiry index is i + 2r + 1. Cap by n.

## Refining the problem, round 2 thoughts
Edge cases:
- r = 0: each station affects only its own city; check reduces to raising individual values.
- Very large k (up to 1e9) — must use 64-bit arithmetic for counts.
- n up to 1e5, station values up to 1e5 => sum(stations) up to 1e10; sums and high bounds must be stored in Python ints (fine).
- Binary search upper bound: sum(stations) + k is safe (no city can get more than all stations).
- Time: O(n log(sumS + k)) which is fine (~1e5 * ~40).

Implementation details:
- Compute base array using prefix sums: base[i] = prefix[min(n-1, i+r)] - prefix[max(0, i-r)-1]
- In feasibility check:
  - Use diff array of length n (all zeros).
  - running_added = 0
  - For each i: running_added += diff[i]; curr = base[i] + running_added
  - If curr < mid: need = mid - curr; if need > remaining_k -> fail; else remaining_k -= need; running_added += need; end = min(n-1, i + 2*r); if end + 1 < n: diff[end+1] -= need
- Return True if loop completes.

Complexities:
- Precompute base: O(n)
- Each check: O(n)
- Binary search iterations: O(log(sumS + k)) up to ~40
- Total: O(n log(sumS + k)) time, O(n) extra space.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxPower(self, stations: List[int], r: int, k: int) -> int:
        n = len(stations)
        # prefix sums
        prefix = [0] * n
        prefix[0] = stations[0]
        for i in range(1, n):
            prefix[i] = prefix[i-1] + stations[i]
        # compute base power for each city: sum of stations in [i-r, i+r]
        base = [0] * n
        for i in range(n):
            left = max(0, i - r)
            right = min(n - 1, i + r)
            base[i] = prefix[right] - (prefix[left - 1] if left > 0 else 0)

        total_existing = prefix[-1]
        lo, hi = 0, total_existing + k  # inclusive upper bound

        def can_achieve(target: int) -> bool:
            # difference array to manage added station contributions
            diff = [0] * (n + 1)  # one extra for easier expiry handling
            running_added = 0
            remaining = k
            for i in range(n):
                running_added += diff[i]
                curr = base[i] + running_added
                if curr < target:
                    need = target - curr
                    if need > remaining:
                        return False
                    remaining -= need
                    running_added += need
                    # place these 'need' stations at position pos = min(n-1, i + r)
                    # their coverage ends at end = min(n-1, pos + r)
                    # For pos = min(n-1, i + r), this end is min(n-1, i + 2*r)
                    end = min(n - 1, i + 2 * r)
                    # subtract from diff at end+1 to expire their effect
                    if end + 1 < len(diff):
                        diff[end + 1] -= need
                # continue
            return True

        ans = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if can_achieve(mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans
```
- Notes:
  - We compute base city powers using prefix sums in O(n).
  - The binary search tries candidate minimum powers; each feasibility check simulates greedy placements using a difference array to amortize added contributions. Each check is O(n).
  - Time complexity: O(n log(sum(stations) + k)). Space complexity: O(n) for base and diff arrays.
  - The greedy choice (placing needed stations at the rightmost position that still covers the current city) maximizes future benefit and is correct when sweeping left-to-right.