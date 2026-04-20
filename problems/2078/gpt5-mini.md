# [Problem 2078: Two Furthest Houses With Different Colors](https://leetcode.com/problems/two-furthest-houses-with-different-colors/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum absolute difference in indices between two houses that have different colors. Brute force would check all pairs (i, j) and track the max |i-j| when colors differ — that's O(n^2). But constraints are small (n <= 100), yet we can do better easily.

Observations:
- The largest possible distance is between index 0 and n-1. If colors[0] != colors[n-1], answer is n-1 immediately.
- If they are equal, one of the farthest differing pairs must involve either index 0 or index n-1 (because pushing one end inward until color changes gives a maximal distance). So we can look for the farthest index from 0 with a different color than colors[0], and the farthest index from n-1 with a different color than colors[n-1], and take the max.

So a two-pass scan from ends yields O(n) time and O(1) space.

## Refining the problem, round 2 thoughts
Edge cases:
- Problem guarantees at least two houses have different colors, so we'll always find a differing house when scanning inward.
- We should stop scanning as soon as we find the first differing house from each end because scanning from the end gives the furthest one.

Alternative approaches:
- Track first and last occurrence of each color and compute pairwise distances — unnecessary overhead for this problem.
- A single pass keeping track of first color and last color comparisons is sufficient.

Time/space:
- Time: O(n) — at most two linear scans.
- Space: O(1) — only a few variables.

## Attempted solution(s)
```python
class Solution:
    def maxDistance(self, colors: List[int]) -> int:
        n = len(colors)
        # If ends differ, that's the maximum possible distance.
        if colors[0] != colors[-1]:
            return n - 1

        ans = 0
        # Find farthest index from left end that has a different color than colors[0].
        for i in range(n - 1, -1, -1):
            if colors[i] != colors[0]:
                ans = max(ans, i - 0)
                break

        # Find farthest index from right end that has a different color than colors[-1].
        for i in range(0, n):
            if colors[i] != colors[-1]:
                ans = max(ans, (n - 1) - i)
                break

        return ans
```
- Notes:
  - Approach: Check if the two ends differ (fast exit). Otherwise, scan from the right for the first index whose color differs from colors[0], giving distance i - 0. Then scan from the left for the first index whose color differs from colors[-1], giving distance (n-1) - i. The maximum of these two is the answer.
  - Time complexity: O(n) — at most two linear scans of the list.
  - Space complexity: O(1) — only constant extra space used.