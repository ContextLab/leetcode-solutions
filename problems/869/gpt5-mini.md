# [Problem 869: Reordered Power of 2](https://leetcode.com/problems/reordered-power-of-2/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Brute force approach that comes to mind first is to generate all permutations of the digits of n and check if any is a power of two. But permutations are factorial in the number of digits (up to 10!), which is too slow.

I notice that there are very few powers of two that matter: for n up to 10^9, powers of two are at most around 2^30. That means there are only ~31 candidate target numbers. So instead of permuting n, I can compare some signature of n's digits (like sorted digits or digit counts) with the signatures of all powers of two. If any match, we can reorder the digits of n into that power of two (and the power string won't have a leading zero), so return true.

Using sorted strings of digits is simple and small-cost because strings are only up to 10 characters. Alternatively, using a 10-length tuple of digit counts is also convenient and avoids sorting.

## Refining the problem, round 2 thoughts
- Precompute signatures (sorted-digit strings or digit-count tuples) for powers of two from 2^0 up to 2^30 (inclusive).
- Compute the signature for n and check membership among the precomputed signatures.
- Edge cases:
  - n = 1 should be true (1 == 2^0).
  - Numbers containing zeros are fine: a matching power of two will not start with zero, so comparing signatures implicitly enforces a valid reordering (no leading zero).
- Complexity:
  - Time: O(1) practically — we compare against at most 31 small strings/tuples; computing sorted string is O(d log d) with d <= 10.
  - Space: O(31 * d) for storing signatures, constant.

I'll implement with sorted strings for clarity.

## Attempted solution(s)
```python
class Solution:
    def reorderedPowerOf2(self, n: int) -> bool:
        s = ''.join(sorted(str(n)))
        # Precompute sorted-digit representations of powers of two up to 2^30
        power_signatures = { ''.join(sorted(str(1 << i))) for i in range(31) }
        return s in power_signatures
```
- Notes:
  - Approach: compute the sorted-digit string ("signature") of n and check if it matches the signature of any power of two (2^0 .. 2^30).
  - Time complexity: O(1) in practice (at most 31 small sorts/compare operations). More precisely, O(D log D) to sort digits of n plus O(31 * D log D) precomputation where D <= 10.
  - Space complexity: O(31 * D) for the set of signatures, which is constant.
  - Implementation detail: using sorted-digit strings implicitly handles the "no leading zero" requirement because a matching power of two string never begins with '0'.