# [Problem 2551: Put Marbles in Bags](https://leetcode.com/problems/put-marbles-in-bags/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I want to understand how the score depends on where we cut the array into k contiguous segments. Each bag is a contiguous subarray [i..j] and its cost is weights[i] + weights[j]. If we split the array into k segments, the total score is the sum of the first and last elements of each segment.

If the whole array is a single segment, the score is weights[0] + weights[n-1]. When we make a cut between i and i+1, that cut creates an additional boundary: it makes weights[i] become the end of a segment and weights[i+1] become the start of the next segment. So each cut contributes (weights[i] + weights[i+1]) to the total score (on top of the baseline weights[0] + weights[n-1]). Thus the total score for any partition into k segments equals weights[0] + weights[n-1] plus the sum of the k-1 chosen adjacent pair sums s_i = weights[i] + weights[i+1] for the cut positions.

Therefore to maximize the score pick the largest k-1 s_i; to minimize pick the smallest k-1 s_i. The difference between max and min scores is the difference between the sum of the largest k-1 s_i and the sum of the smallest k-1 s_i. If k == 1 (no cuts) the difference is 0.

This suggests computing all n-1 pair sums, sorting them, and taking the top and bottom k-1 sums.

## Refining the problem, round 2 thoughts
Edge cases:
- k = 1: no cuts, difference = 0.
- k = n: k-1 = n-1, which picks every adjacent pair; max and min sums are equal, difference = 0.
- weights length up to 1e5, weights up to 1e9: pair sums up to 2e9, sums up to ~2e14 — fit in Python int easily.

Complexity:
- Build the n-1 pair sums: O(n) time and O(n) extra space.
- Sorting them: O(n log n) time.
- Summation for top/bottom k-1: O(k) but k <= n so included.

We could do it in O(n) time using selection (nth_element) or two heaps to avoid full sort, but O(n log n) is fine for 1e5.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def putMarbles(self, weights: List[int], k: int) -> int:
        n = len(weights)
        if k == 1:
            return 0
        
        # compute adjacent pair sums s_i = weights[i] + weights[i+1] for i in [0..n-2]
        pairs = [weights[i] + weights[i+1] for i in range(n-1)]
        pairs.sort()
        
        # sum of smallest k-1
        small_sum = sum(pairs[:k-1])
        # sum of largest k-1
        large_sum = sum(pairs[-(k-1):]) if k-1 > 0 else 0
        
        return large_sum - small_sum
```
- Notes: The solution computes the (n-1) adjacent pair sums, sorts them, and returns the difference between the sum of the largest k-1 and the sum of the smallest k-1 pair sums. Time complexity: O(n log n) due to sorting. Space complexity: O(n) for the pair sums array. This handles all edge cases including k == 1 or k == n.