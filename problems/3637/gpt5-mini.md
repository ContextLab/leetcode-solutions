# [Problem 3637: Trionic Array I](https://leetcode.com/problems/trionic-array-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to check whether the array can be split (with overlapping endpoints) into three contiguous segments: strictly increasing from index 0 to p, strictly decreasing from p to q, and strictly increasing from q to n-1, where 0 < p < q < n-1. That means p must be at least 1 and at most n-3, q at least p+1 and at most n-2.

A direct approach: precompute which prefixes are strictly increasing and which suffixes are strictly increasing. For each candidate p that satisfies the prefix condition, try to walk a strictly decreasing run starting at p and see if any q in that run satisfies the suffix (increasing) condition. n is at most 100, so an O(n^2) solution is fine. Need to be careful with strict comparisons and boundaries.

## Refining the problem, round 2 thoughts
- Compute inc_prefix[i] = True if nums[0..i] is strictly increasing.
- Compute inc_suffix[i] = True if nums[i..n-1] is strictly increasing.
- For each p in range(1, n-2 + 1) (i.e. 1..n-3) with inc_prefix[p] true, iterate q from p+1 forward while nums[k-1] > nums[k] to ensure the p..q segment is strictly decreasing. For each q in that decreasing run check if inc_suffix[q] is true (and q < n-1 holds because inc_suffix[n-1] is true but q must be < n-1 — our q iteration will stop before n-1).
- If any such pair exists, return True; otherwise return False.

Edge cases:
- Small n (e.g., n = 3) — impossible to have 0 < p < q < n-1, so return False.
- Equal adjacent elements break strict monotonicity.
Time complexity: O(n^2) worst-case (n ≤ 100), space O(n).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def isTrionic(self, nums: List[int]) -> bool:
        n = len(nums)
        # need 0 < p < q < n-1, so at least n >= 4 to be possible
        if n < 4:
            return False

        # inc_prefix[i] = True if nums[0..i] is strictly increasing
        inc_prefix = [False] * n
        inc_prefix[0] = True
        for i in range(1, n):
            inc_prefix[i] = inc_prefix[i-1] and (nums[i-1] < nums[i])

        # inc_suffix[i] = True if nums[i..n-1] is strictly increasing
        inc_suffix = [False] * n
        inc_suffix[n-1] = True
        for i in range(n-2, -1, -1):
            inc_suffix[i] = inc_suffix[i+1] and (nums[i] < nums[i+1])

        # try each possible p (1 .. n-3)
        for p in range(1, n-2):
            if not inc_prefix[p]:
                continue
            # walk q from p+1 while strictly decreasing nums[p..q]
            q = p + 1
            # we can only consider q up to n-2 (since q < n-1)
            while q <= n-2 and nums[q-1] > nums[q]:
                # if suffix from q to end is strictly increasing, we found valid p,q
                if inc_suffix[q]:
                    return True
                q += 1

        return False
```
- Notes on approach: We precompute prefix/suffix strict-increasing flags, then for each valid prefix end p we scan the strictly decreasing run starting at p to find a q that also starts a strictly increasing suffix. This directly enforces the required three-segment shape.
- Complexity: Time O(n^2) in the worst case because each p might scan a decreasing run; n ≤ 100 so this is fine. Space O(n) for the prefix/suffix arrays.