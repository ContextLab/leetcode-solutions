# [Problem 3635: Earliest Finish Time for Land and Water Rides II](https://leetcode.com/problems/earliest-finish-time-for-land-and-water-rides-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We must pick exactly one land and one water ride in either order. For a chosen pair (land i, water j) if we do land -> water:
- Start land at landStartTime[i] (starting later only delays everything), finish at Lend = landStartTime[i] + landDuration[i].
- We can start water at max(waterStartTime[j], Lend) and finish at max(waterStartTime[j], Lend) + waterDuration[j].
So finish = max(Lend, waterStartTime[j]) + waterDuration[j].

Similarly water -> land finish = max(waterStartTime[j] + waterDuration[j], landStartTime[i]) + landDuration[i].

Brute force over all pairs would be O(n*m) (n, m up to 5e4 — too big). Notice structure: for a fixed land ride (fixed Lend), the best water ride choice splits into two types:
- water rides with waterStart <= Lend: finish = Lend + waterDuration[j] => among those choose minimal waterDuration.
- water rides with waterStart > Lend: finish = waterStart[j] + waterDuration[j] => among those choose minimal waterStart+waterDuration.

So if we sort water rides by start time and precompute prefix min of waterDuration and suffix min of start+duration, we can answer best water-for-a-given-Lend in O(log m) (binary search) or O(1) if we sweep. Symmetrically handle water-first option by sorting land rides similarly.

## Refining the problem, round 2 thoughts
Plan:
- Sort water rides by waterStart ascending; build arrays starts_w, dur_w.
- Build prefix_min_dur_w[i] = min(dur_w[0..i]) and suffix_min_start_plus_dur_w[i] = min(starts_w[k] + dur_w[k] for k >= i).
- For each land ride with Lend = landStart + landDur:
  - binary search largest index idx such that starts_w[idx] <= Lend.
  - candidate1 = Lend + prefix_min_dur_w[idx] (if idx >= 0)
  - candidate2 = suffix_min_start_plus_dur_w[idx+1] (if idx+1 < m)
  - best for this land->water is min of valid candidates.
- Do analogous preprocessing for land rides and for each water ride consider water->land case.
- Answer is global min over all these candidates.

Edge cases:
- idx may be -1 (no water starts <= Lend) or idx = m-1 (no water starts > Lend).
- Use large INF for invalid candidates.
Complexities:
- Sorting O(m log m + n log n)
- Precomputations O(m + n)
- For each ride binary search O(log m) (or O(log n)), so total O(n log m + m log n). With sorting dominates, overall O(n log n + m log m). Space O(n + m).

This is efficient for constraints.

## Attempted solution(s)
```python
from bisect import bisect_right
import math

class Solution:
    def earliestFinishTime(self, landStartTime, landDuration, waterStartTime, waterDuration) -> int:
        n = len(landStartTime)
        m = len(waterStartTime)
        INF = 10**18

        # Preprocess water rides: sort by start time
        water = sorted(zip(waterStartTime, waterDuration))
        ws = [w for w, d in water]
        wd = [d for w, d in water]

        # prefix minimum of water durations (for ws <= Lend)
        prefix_min_wd = [INF] * m
        cur = INF
        for i in range(m):
            cur = min(cur, wd[i])
            prefix_min_wd[i] = cur

        # suffix minimum of ws + wd (for ws > Lend)
        suffix_min_ws_plus_wd = [INF] * m
        cur = INF
        for i in range(m-1, -1, -1):
            cur = min(cur, ws[i] + wd[i])
            suffix_min_ws_plus_wd[i] = cur

        ans = INF

        # For each land ride consider land -> water
        for i in range(n):
            Lstart = landStartTime[i]
            Ldur = landDuration[i]
            Lend = Lstart + Ldur

            # find rightmost index with ws[idx] <= Lend
            idx = bisect_right(ws, Lend) - 1

            cand = INF
            if idx >= 0:
                # some water rides open at or before Lend
                cand = min(cand, Lend + prefix_min_wd[idx])
            if idx + 1 < m:
                # some water rides open after Lend
                cand = min(cand, suffix_min_ws_plus_wd[idx+1])
            if cand < ans:
                ans = cand

        # Preprocess land rides similarly for water -> land
        land = sorted(zip(landStartTime, landDuration))
        ls = [l for l, d in land]
        ld = [d for l, d in land]

        prefix_min_ld = [INF] * n
        cur = INF
        for i in range(n):
            cur = min(cur, ld[i])
            prefix_min_ld[i] = cur

        suffix_min_ls_plus_ld = [INF] * n
        cur = INF
        for i in range(n-1, -1, -1):
            cur = min(cur, ls[i] + ld[i])
            suffix_min_ls_plus_ld[i] = cur

        # For each water ride consider water -> land
        for j in range(m):
            Wstart = ws[j]
            Wdur = wd[j]
            Wend = Wstart + Wdur

            idx = bisect_right(ls, Wend) - 1

            cand = INF
            if idx >= 0:
                cand = min(cand, Wend + prefix_min_ld[idx])
            if idx + 1 < n:
                cand = min(cand, suffix_min_ls_plus_ld[idx+1])
            if cand < ans:
                ans = cand

        return ans
```
- Notes:
  - We always start the first ride at its earliest opening time (no benefit to delaying).
  - Sorting and prefix/suffix minima let us find the best second ride for any given first ride in O(log N) for the binary search.
  - Time complexity: O(n log n + m log m) dominated by sorting (and binary searches add O(n log m + m log n) but still within same bounds).
  - Space complexity: O(n + m) for auxiliary arrays.