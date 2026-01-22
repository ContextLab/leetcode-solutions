# [Problem 2106: Maximum Fruits Harvested After at Most K Steps](https://leetcode.com/problems/maximum-fruits-harvested-after-at-most-k-steps/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have fruits at discrete positions on a line sorted by position. Starting at startPos and with at most k steps total, we can move left or right and collect all fruits we touch. We want the maximum total amount of fruits collected.

This looks like a sliding-window / two-pointer + prefix-sum problem: we want to pick a contiguous interval of positions [i, j] to visit (since moving along the line, visiting positions that are not contiguous would only waste steps). For any interval [i, j] (positions pos[i]..pos[j]) we can compute the minimum number of steps required to start at startPos, visit every position in the interval, and stop anywhere. There are three geometry cases:
- Entire interval is left of startPos,
- Entire interval is right of startPos,
- Interval spans startPos.

We can compute the minimal steps for each case. Then we can slide a window [l, r] over the sorted positions, maintain the sum via prefix sums, and ensure the minimal steps <= k. Two-pointer seems applicable because as r increases the required steps never decreases for fixed l, so we can increase l when the window becomes infeasible.

## Refining the problem, round 2 thoughts
Define cost(l, r): minimal steps to collect all fruits from pos[l]..pos[r] starting at startPos. Cases:
- If pos[r] <= startPos (all left): cost = startPos - pos[l] (go left to leftmost).
- If pos[l] >= startPos (all right): cost = pos[r] - startPos (go right to rightmost).
- Otherwise (pos[l] <= startPos <= pos[r]): cost = (pos[r] - pos[l]) + min(startPos - pos[l], pos[r] - startPos). This matches the two patterns (go left first then right or right first then left).

Algorithm:
- Build prefix sums of amounts to get interval sums in O(1).
- Two pointers l = 0, iterate r from 0..n-1:
  - While window [l, r] has cost > k, increment l.
  - When cost <= k, consider the sum of fruits in [l, r] as candidate.
This is O(n) time and O(n) space. Careful with edge cases where no positions are reachable — the algorithm handles that (sum zero).

Time complexity: O(n).
Space complexity: O(n) for prefix sums.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxTotalFruits(self, fruits: List[List[int]], startPos: int, k: int) -> int:
        n = len(fruits)
        pos = [p for p, a in fruits]
        amt = [a for p, a in fruits]
        # prefix sums
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i+1] = pref[i] + amt[i]

        def interval_sum(l: int, r: int) -> int:
            return pref[r+1] - pref[l]

        def cost(l: int, r: int) -> int:
            # minimal steps to collect all fruits in [l, r] starting at startPos
            if pos[r] <= startPos:
                # entirely to the left
                return startPos - pos[l]
            if pos[l] >= startPos:
                # entirely to the right
                return pos[r] - startPos
            # spans startPos
            return (pos[r] - pos[l]) + min(startPos - pos[l], pos[r] - startPos)

        ans = 0
        l = 0
        for r in range(n):
            # advance l while window infeasible
            while l <= r and cost(l, r) > k:
                l += 1
            if l <= r:
                ans = max(ans, interval_sum(l, r))
        return ans
```
- Notes about the solution:
  - We maintain a sliding window [l, r] over sorted fruit positions. For each r we push l forward until the minimal steps to cover [l, r] is <= k.
  - interval_sum uses prefix sums to get the total fruits in O(1).
  - cost(l, r) covers three geometric cases (all left, all right, spanning start).
  - Time complexity: O(n) because each of l and r moves at most n steps.
  - Space complexity: O(n) for the prefix sum and arrays extracted from input.
  - This solution handles the edge cases:
    - No reachable fruits -> ans stays 0.
    - All fruits on one side or mixed sides are accounted correctly.