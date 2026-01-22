# [Problem 2145: Count the Hidden Sequences](https://leetcode.com/problems/count-the-hidden-sequences/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share my internal chain-of-thought, but here is a concise summary of the approach: compute the running prefix sums of differences (treating the first hidden element as 0), track the minimum and maximum prefix values. If the first element x is chosen, all hidden elements are x + prefix[i]; to fit within [lower, upper] we need x in the intersection [lower - min_prefix, upper - max_prefix]. The number of integer choices for x in that interval (if any) is the answer.

## Refining the problem, round 2 thoughts
- We only need the running sum, min and max; no need to store the full prefix array.
- If min_prefix = a and max_prefix = b, allowed x satisfy: lower - a <= x <= upper - b.
- The count is max(0, (upper - b) - (lower - a) + 1).
- Edge cases: if the interval is empty result is 0. Works when differences contains negative/positive values and large n.
- Time complexity O(n), space O(1) (aside from input).

## Attempted solution(s)
```python
class Solution:
    def numberOfArrays(self, differences: list[int], lower: int, upper: int) -> int:
        # running prefix starting from 0, track min and max prefix values
        pref = 0
        min_pref = 0
        max_pref = 0
        for d in differences:
            pref += d
            if pref < min_pref:
                min_pref = pref
            if pref > max_pref:
                max_pref = pref

        # x must satisfy: lower - min_pref <= x <= upper - max_pref
        left = lower - min_pref
        right = upper - max_pref
        if right < left:
            return 0
        return right - left + 1
```
- Notes:
  - Approach: compute running prefix sums of differences (as offsets from hidden[0]), then derive allowed range for hidden[0].
  - Time complexity: O(n) where n = len(differences).
  - Space complexity: O(1) extra space (only counters and min/max tracked).
  - Implementation detail: we start prefix at 0 representing hidden[0] = x, so hidden[i] = x + prefix[i]; prefix[0] = 0, prefix[i] = sum of differences up to i-1.