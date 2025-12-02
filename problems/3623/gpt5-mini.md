# [Problem 3623: Count Number of Trapezoids I](https://leetcode.com/problems/count-number-of-trapezoids-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count convex quadrilaterals with at least one pair of horizontal sides. The simplest realization: any trapezoid with horizontal sides uses two distinct y-levels (top and bottom). On each of those y-levels we must pick 2 distinct points (a horizontal segment). So for a pair of distinct y-levels y1 and y2, if y1 has A points (choose C(A,2) horizontal segments) and y2 has B points (C(B,2)), then naive total possibilities for that pair is C(A,2)*C(B,2). But not all such choices produce a valid trapezoid: if the top segment is strictly to the left of the bottom segment (their x-intervals disjoint) or strictly to the right, the four points do not form a convex quadrilateral with horizontal top & bottom. So for each pair of y-levels we must subtract the number of choices where the two horizontal segments are disjoint (top entirely left of bottom, or vice-versa). Summing over all pairs of y's directly is O(Y^2) which is too large (Y up to N).

We need a global trick to avoid pairwise y enumeration. Note that total sum over unordered pairs of y's of C(A,2)*C(B,2) can be computed from the per-row values s_y = C(cnt_y,2) using combinatorics (sum_{i<j} s_i * s_j). The challenge is to compute the total number of disjoint configurations across all unordered y-pairs efficiently. We can view disjoint configurations as those where there exists a vertical split (between two adjacent x coordinates) so that both chosen points for the top y are strictly left of the split and both chosen points for the bottom y are strictly right. Summing over splits we can aggregate contributions across all y-pairs efficiently: for each split, compute sum_left = sum_y C(left_count_y, 2) and sum_right = sum_y C(right_count_y, 2); naive multiplication counts also the cases where top and bottom are the same y, so subtract sum_y C(left_count_y,2)*C(right_count_y,2). Summing this over splits yields the total number of ordered disjoint pairs where "top is left of bottom". That exactly equals the total disjoint (both directions) we must subtract from the total pair count. This leads to an O(N log N) (sorting x's) and O(N) scan solution.

## Refining the problem, round 2 thoughts
Edge cases:
- Many points can share same x; we must move all points at a given x together and then consider the split after that x.
- We must ensure we always deal with distinct y-levels for top and bottom (we subtract same-y contributions when computing disjoint per-split).
- Use integer arithmetic carefully; answer mod 1e9+7.
- Complexity: building maps O(N), sorting unique x's O(Ux log Ux) <= O(N log N), scanning and updating counts O(N). Memory O(N).

Proof sketch of correctness:
- totalPairsSum = sum_{unordered y1<y2} C(cnt[y1],2)*C(cnt[y2],2) computed via (sum s_y^2 trick).
- For disjoint pairs we computed S = sum over splits (sum_left * sum_right - sum_y leftC2[y]*rightC2[y]). sum_left*sum_right counts ordered pairs (y_top,y_bottom) with top pair both left and bottom pair both right, including y_top==y_bottom; subtracting per-y product removes those same-y cases. Summing splits enumerates all ordered disjoint configurations exactly once (a disjoint configuration has a unique gap between max(x of top segment) and min(x of bottom segment) which is captured by one split). Finally total overlapping trapezoids = totalPairsSum - S. Return modulo.

## Attempted solution(s)
```python
from collections import defaultdict

MOD = 10**9 + 7

class Solution:
    def countTrapezoids(self, points: list[list[int]]) -> int:
        # Map y -> list of x's
        y_to_xs = defaultdict(list)
        # Map x -> list of y's (we will use y indices)
        x_to_ys = defaultdict(list)
        for x, y in points:
            y_to_xs[y].append(x)
            x_to_ys[x].append(y)

        # Assign an index to each distinct y for compact arrays
        y_list = list(y_to_xs.keys())
        y_index = {y: i for i, y in enumerate(y_list)}
        m = len(y_list)

        # cnt_y, and initial right counts (all points are to the right of initial split)
        cnt = [0] * m
        for y, xs in y_to_xs.items():
            idx = y_index[y]
            cnt[idx] = len(xs)

        def C2(k: int) -> int:
            return k * (k - 1) // 2

        # s_y = C(cnt_y, 2)
        s = [C2(c) for c in cnt]
        sum_s = sum(s)

        # total pairs over unordered y-pairs = sum_{i<j} s_i * s_j
        # = (sum_s^2 - sum(s_i^2)) // 2
        total_pairs = (sum_s * sum_s - sum(x*x for x in s)) // 2

        # Prepare scanning over x splits:
        # left_cnt and right_cnt per y
        left_cnt = [0] * m
        right_cnt = cnt[:]  # copy

        leftC2 = [0] * m
        rightC2 = [C2(r) for r in right_cnt]

        sum_left = 0
        sum_right = sum(rightC2)
        cross = 0  # sum of leftC2[i] * rightC2[i]

        # iterate x in increasing order; move all points at that x from right to left,
        # then consider the split after this x
        S = 0
        for x in sorted(x_to_ys.keys()):
            # move all points at x
            for y in x_to_ys[x]:
                idx = y_index[y]
                old_leftC2 = leftC2[idx]
                old_rightC2 = rightC2[idx]

                # update counts
                left_cnt[idx] += 1
                right_cnt[idx] -= 1

                new_leftC2 = C2(left_cnt[idx])
                new_rightC2 = C2(right_cnt[idx])

                leftC2[idx] = new_leftC2
                rightC2[idx] = new_rightC2

                # update aggregates
                sum_left += new_leftC2 - old_leftC2
                sum_right += new_rightC2 - old_rightC2
                cross += new_leftC2 * new_rightC2 - old_leftC2 * old_rightC2

            # After moving all points at x, consider split after x:
            # Contribution to ordered disjoint (top-left-of-bottom) at this split:
            # sum_left * sum_right - sum_i leftC2[i] * rightC2[i]
            S += sum_left * sum_right - cross

        # total disjoint across both directions (unordered) equals S (we counted ordered disjoint top-left-of-bottom across splits)
        total_trapezoids = total_pairs - S
        ans = total_trapezoids % MOD
        return ans
```
- Notes:
  - We grouped points by y to compute s_y = C(cnt_y,2).
  - total_pairs (all ways to pick two horizontal segments on two different y-levels) computed in O(#y).
  - We compute S by scanning x positions; after moving all points at an x to the "left" side, we compute contribution of that split. Updates per point are O(1): adjust left/right C2 values and aggregates.
  - Complexity: O(N log N) due to sorting unique x values; O(N) additional time and O(N) space for maps/arrays.
  - Correctness: explained above.