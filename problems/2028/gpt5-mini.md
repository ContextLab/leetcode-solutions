# [Problem 2028: Find Missing Observations](https://leetcode.com/problems/find-missing-observations/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We know the total number of rolls is n + m and the desired average is mean, so the total sum must be mean * (n + m). We have m observed rolls (values 1..6) with known sum. The missing n rolls must sum to missing_sum = total_needed - sum(observed). Each missing roll must be an integer between 1 and 6. So we need to check whether missing_sum is achievable with n numbers in [1,6]: that means n*1 <= missing_sum <= n*6. If impossible, return [].

If possible, we need to construct any array of length n whose entries are integers in [1,6] summing to missing_sum. A straightforward approach: start with all ones (sum = n), then distribute the remaining remaining = missing_sum - n among the n entries, adding at most 5 to each (since 1+5 = 6). Iterate through entries and add min(5, remaining) to each until remaining is 0. This yields a valid array.

## Refining the problem, round 2 thoughts
Edge cases:
- missing_sum negative (total needed less than observed sum): impossible
- missing_sum too small (< n) or too large (> 6*n): impossible
- remaining distribution should not overflow the 6 bound: using min(5, remaining) per slot enforces that.

Complexity considerations:
- Summing observed rolls is O(m).
- Building the result array is O(n).
- Memory: O(n) for output (required). No extra large structures.

This greedy fill-from-1 works because any distribution can be transformed into this bounded distribution by repeatedly moving units from higher to lower entries; greedy is sufficient to produce one valid configuration.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def missingRolls(self, rolls: List[int], mean: int, n: int) -> List[int]:
        m = len(rolls)
        total_needed = mean * (n + m)
        observed_sum = sum(rolls)
        missing_sum = total_needed - observed_sum

        # Check feasibility: each missing roll must be between 1 and 6
        if missing_sum < n or missing_sum > 6 * n:
            return []

        # Start with all ones, then distribute the remaining (missing_sum - n)
        res = [1] * n
        remaining = missing_sum - n  # amount left to distribute, each slot can take up to +5

        idx = 0
        while remaining > 0 and idx < n:
            add = min(5, remaining)
            res[idx] += add
            remaining -= add
            idx += 1

        return res
```
- Notes:
  - Approach: compute required missing sum, check bounds [n, 6*n], construct result by starting with ones and greedily adding up to 5 to each entry until the remaining sum is distributed.
  - Time complexity: O(m + n) — summing rolls takes O(m), building the result takes O(n).
  - Space complexity: O(n) for the returned array (plus O(1) extra).
  - This returns any valid array; the distribution order is arbitrary (we fill left-to-right).