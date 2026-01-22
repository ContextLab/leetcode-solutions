# [Problem 1395: Count Number of Teams](https://leetcode.com/problems/count-number-of-teams/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share my internal chain-of-thought or stream-of-consciousness. I can, however, give a concise high-level approach: For every soldier chosen as the middle element j, count how many soldiers to the left have ratings smaller/greater than rating[j] and how many to the right have ratings smaller/greater than rating[j]. The number of increasing teams with j as the middle is left_smaller * right_greater, and the number of decreasing teams is left_greater * right_smaller. Sum over all j.

## Refining the problem, round 2 thoughts
I can’t provide step-by-step internal deliberation, but here is a concise refinement and edge-case summary:
- Ratings are unique, so no equal comparisons to handle.
- A straightforward O(n^2) solution is simple and fast enough for n ≤ 1000: for each j, scan left and right to compute counts.
- There is also an O(n log n) approach using Fenwick/BIT or segment trees if needed for larger n.
- Edge cases: n < 3 -> 0 (constraints guarantee n ≥ 3), typical unique ratings handled by simple comparisons.

## Attempted solution(s)
```python
class Solution:
    def numTeams(self, rating: list[int]) -> int:
        n = len(rating)
        ans = 0
        for j in range(n):
            left_smaller = left_greater = 0
            right_smaller = right_greater = 0
            # count on the left of j
            for i in range(j):
                if rating[i] < rating[j]:
                    left_smaller += 1
                else:
                    left_greater += 1
            # count on the right of j
            for k in range(j+1, n):
                if rating[k] < rating[j]:
                    right_smaller += 1
                else:
                    right_greater += 1
            # increasing sequences: left_smaller * right_greater
            # decreasing sequences: left_greater * right_smaller
            ans += left_smaller * right_greater + left_greater * right_smaller
        return ans
```
- Notes:
  - Approach: For each index j as the middle of the trio, compute counts of smaller/greater ratings on both sides and add the products for increasing and decreasing teams.
  - Time complexity: O(n^2) — for each of the n possible middle indices we scan up to O(n) elements left and right.
  - Space complexity: O(1) additional space (only counters used).
  - This is simple, clear, and fits constraints (n ≤ 1000). For much larger n, consider coordinate compression + Fenwick tree to get O(n log n).