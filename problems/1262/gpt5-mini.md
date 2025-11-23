# [Problem 1262: Greatest Sum Divisible by Three](https://leetcode.com/problems/greatest-sum-divisible-by-three/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I want the largest sum from some subset of the array such that the sum % 3 == 0. The simplest idea is to take as many numbers as possible — i.e., try to use the total sum, and if total % 3 != 0, remove the smallest possible amount to make it divisible by 3. So compute total = sum(nums). If total % 3 == 0 we're done. Otherwise, depending on remainder r (1 or 2), either remove the smallest single number with num % 3 == r, or remove the smallest two numbers whose remainders sum to r (i.e., two with remainder 3-r). We should track the smallest one or two numbers in each remainder class. This is O(n) and constant extra space.

I also recall a DP approach where we keep dp[0..2] = max sum with remainder 0,1,2 and update for each number, but the greedy "remove minimal" approach is simpler to implement.

Edge cases: if no appropriate numbers exist to remove we must return 0 because we can choose empty subset. Also handle when array has small size (1 or 2).

## Refining the problem, round 2 thoughts
Refinements:
- Efficiently track the two smallest numbers for remainder 1 and remainder 2 classes. Initialize them to infinity and update while iterating.
- After iteration, if total % 3 == 1: candidate removals are min_single_mod1 and sum_of_two_smallest_mod2. If neither exists, answer is 0. Likewise for remainder 2.
- Complexity: O(n) time, O(1) extra space.
- Alternative solution: DP with dp = [0, -inf, -inf], then for each num update new_dp[(j + num%3)%3] = max(dp[(j + num%3)%3], dp[j] + num) — also O(n) time and O(1) space.
- Confirm with examples: [3,6,5,1,8] -> total 23 remainder 2 -> remove smallest mod2 (5) or two mod1s (1 and 8? 8%3=2, so not) so remove 5 get 18.
- Edge-case: if removal candidates sum to more than total just silly; check existence via infinity sentinel.

## Attempted solution(s)
```python
from typing import List
import math

class Solution:
    def greatestSumDivisibleByThree(self, nums: List[int]) -> int:
        total = sum(nums)
        # track smallest two numbers with remainder 1 and remainder 2
        inf = float('inf')
        m1_a = m1_b = inf  # two smallest with num % 3 == 1
        m2_a = m2_b = inf  # two smallest with num % 3 == 2

        for x in nums:
            r = x % 3
            if r == 1:
                # update two smallest for remainder 1
                if x < m1_a:
                    m1_b = m1_a
                    m1_a = x
                elif x < m1_b:
                    m1_b = x
            elif r == 2:
                # update two smallest for remainder 2
                if x < m2_a:
                    m2_b = m2_a
                    m2_a = x
                elif x < m2_b:
                    m2_b = x

        rem = total % 3
        if rem == 0:
            return total

        ans = 0
        if rem == 1:
            # Option 1: remove smallest single remainder-1
            cand1 = total - m1_a if m1_a != inf else -math.inf
            # Option 2: remove two smallest remainder-2
            cand2 = total - (m2_a + m2_b) if m2_a != inf and m2_b != inf else -math.inf
            ans = max(0, int(max(cand1, cand2)))  # ensure non-negative
        else:  # rem == 2
            # Option 1: remove smallest single remainder-2
            cand1 = total - m2_a if m2_a != inf else -math.inf
            # Option 2: remove two smallest remainder-1
            cand2 = total - (m1_a + m1_b) if m1_a != inf and m1_b != inf else -math.inf
            ans = max(0, int(max(cand1, cand2)))

        return ans
```
- Notes:
  - Approach: Greedy removal of the smallest total value necessary to make the sum divisible by 3. Track the two smallest numbers in remainder classes 1 and 2 while scanning once.
  - Time complexity: O(n) where n = len(nums), because we scan the array once.
  - Space complexity: O(1) extra space (only a few variables).
  - Alternative: A DP approach using dp[3] to keep max sums for each remainder class also works and is equally O(n) time, O(1) space.