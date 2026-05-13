# [Problem 1674: Minimum Moves to Make Array Complementary](https://leetcode.com/problems/minimum-moves-to-make-array-complementary/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see we can pair indices i and n-1-i; each pair (a,b) contributes independently to the target sum S = nums[i] + nums[n-1-i]. For a fixed target S (2..2*limit), each pair needs 0, 1, or 2 moves:
- 0 moves if a+b == S
- 1 move if by changing one element from the pair we can make their sum S (i.e., S in [min(a,b)+1, max(a,b)+limit])
- otherwise 2 moves

We could try all S and compute cost by checking each pair, but that would be O(n * limit) in worst case. Instead we can aggregate pair contributions for all S using counting and prefix/difference arrays to get O(n + limit).

## Refining the problem, round 2 thoughts
Refinement:
- For each pair (a,b) compute:
  - sum_ab = a+b (counts for 0-move case)
  - low = min(a,b) + 1 and high = max(a,b) + limit (the inclusive range of S values that require at most 1 move)
- Maintain:
  - countSum[S] = number of pairs already summing to S (0-move)
  - rangeCount[S] = number of pairs for which S is reachable with exactly 1 move (we compute via difference array over [low, high])
- For each S: total moves = 2*m - rangeCount[S] - countSum[S], where m = n//2. (Start from 2 moves per pair, subtract 1 for each pair covered by the 1-move range, subtract 1 more for pairs exactly equal to S.)
Edge cases: bounds on arrays: S ranges 2..2*limit inclusive. Complexity: we process each pair once (O(n)), then sweep sums 2..2*limit (O(limit)). Space O(limit). This fits constraints.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minMoves(self, nums: List[int], limit: int) -> int:
        n = len(nums)
        m = n // 2
        maxSum = 2 * limit

        # countSum[s] = number of pairs that already sum to s (0 moves needed)
        countSum = [0] * (maxSum + 1)

        # diff to build rangeCount via prefix: for each pair, increment diff[low] and decrement diff[high+1]
        diff = [0] * (maxSum + 2)  # +2 to safely index high+1 up to maxSum+1

        for i in range(m):
            a = nums[i]
            b = nums[n - 1 - i]
            s = a + b
            countSum[s] += 1
            low = min(a, b) + 1
            high = max(a, b) + limit
            # mark the inclusive range [low, high] for which the pair can be done in at most 1 move
            # but we only care for sums in [2..maxSum]; low/high are within that range by construction
            diff[low] += 1
            diff[high + 1] -= 1

        # build rangeCount via prefix sums
        rangeCount = [0] * (maxSum + 1)
        cur = 0
        for s in range(2, maxSum + 1):
            cur += diff[s]
            rangeCount[s] = cur

        # compute minimal moves across all possible sums S
        # base moves if every pair required 2 moves: 2*m
        best = 2 * m
        for s in range(2, maxSum + 1):
            moves = 2 * m - rangeCount[s] - countSum[s]
            if moves < best:
                best = moves

        return best
```
- Notes:
  - Approach: For each pair (a,b) we mark the range of S values achievable with 1 move via a difference array and count exact sums for 0-move cases. For each S, moves = 2*m - (#pairs needing ≤1 move) - (#pairs needing 0 moves as subset), which simplifies as used.
  - Time complexity: O(n + limit) — we iterate over n/2 pairs and then sweep sums from 2 to 2*limit.
  - Space complexity: O(limit) for the auxiliary arrays (diff, countSum, rangeCount).