# [Problem 2818: Apply Operations to Maximize Score](https://leetcode.com/problems/apply-operations-to-maximize-score/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to maximize a product by applying up to k operations. Each operation picks a subarray and within it picks the element with the highest "prime score" (number of distinct prime factors); ties choose the leftmost. Observing that every operation effectively selects a particular index i (the chosen element) and multiplies the score by nums[i]. The same index i can be the chosen element for many different subarrays — specifically for those subarrays where i is the maximum prime-score element and is the leftmost among ties inside the subarray.

So for each index i we can count how many subarrays make i the selected element. If that count is cnt[i], we can select i up to cnt[i] times (each corresponds to choosing a distinct subarray). To maximize the product, pick the largest nums[i] values as many times as possible (greedy by value), consuming k picks. So the problem reduces to:
- compute prime-score P[i] for nums[i]
- compute, for each i, the number of subarrays where i is the chosen index (based on P and tie rule)
- sort indices by nums[i] descending and greedily apply up to k selections using cnt[i] as available multiplicity

Key detail: tie-breaking (leftmost when equal P) affects how we compute the ranges. For i to be chosen for a subarray, there must be no element to the left inside subarray with P >= P[i] (an equal P to the left blocks i), and no element to the right inside subarray with P > P[i] (a strictly greater to the right blocks i). This suggests nearest previous index with P >= P[i] and next index with P > P[i] bounds. Monotonic stacks can compute these efficiently.

## Refining the problem, round 2 thoughts
Refine how to compute boundaries:
- prev[i] = nearest index to left with P[prev] >= P[i] (or -1 if none)
  - Use a monotonic stack that keeps indices with non-decreasing P; while top has P < P[i], pop; top is prev (or -1).
- next[i] = nearest index to right with P[next] > P[i] (or n if none)
  - Traverse from right with a stack keeping strictly decreasing P; while top has P <= P[i], pop; top is next (or n).

Then cnt[i] = (i - prev[i]) * (next[i] - i). These counts sum to n*(n+1)/2 (all subarrays counted exactly once in terms of chosen index).

Finally, sort indices by nums[i] descending, for each index take t = min(cnt[i], k) and multiply ans by nums[i]^t (mod 1e9+7), subtract t from k, stop when k == 0.

Complexity:
- computing prime-scores up to maxA = max(nums) using a sieve-like loop: O(maxA log log maxA + (sum of multiples loops)) ~ O(maxA log log maxA) practically (maxA <= 1e5).
- computing prev/next: O(n)
- sorting indices: O(n log n)
- total: O(maxA log log maxA + n log n), space O(maxA + n).

Edge cases:
- nums contains 1 (prime score 0) — handled.
- large k (up to 1e9) — counts cnt[i] are up to n(n+1)/2; pow(x, t, MOD) handles large exponent efficiently.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maximumScore(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        if n == 0:
            return 1

        maxA = max(nums)

        # Sieve-like count of distinct prime factors for every number up to maxA
        prime_count = [0] * (maxA + 1)
        for p in range(2, maxA + 1):
            if prime_count[p] == 0:  # p is prime
                for multiple in range(p, maxA + 1, p):
                    prime_count[multiple] += 1

        P = [prime_count[x] for x in nums]

        # prev[i] = nearest index to the left with P[prev] >= P[i], or -1 if none
        prev = [-1] * n
        stack = []
        for i in range(n):
            # pop indices with strictly smaller prime-score
            while stack and P[stack[-1]] < P[i]:
                stack.pop()
            prev[i] = stack[-1] if stack else -1
            stack.append(i)

        # next[i] = nearest index to the right with P[next] > P[i], or n if none
        next_idx = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            # pop indices with prime-score <= P[i], leaving > P[i] if any
            while stack and P[stack[-1]] <= P[i]:
                stack.pop()
            next_idx[i] = stack[-1] if stack else n
            stack.append(i)

        # count of subarrays for which i is the chosen element
        counts = [0] * n
        for i in range(n):
            left_choices = i - prev[i]
            right_choices = next_idx[i] - i
            counts[i] = left_choices * right_choices

        # sort indices by value descending
        indices = list(range(n))
        indices.sort(key=lambda i: nums[i], reverse=True)

        ans = 1
        remaining = k
        for idx in indices:
            if remaining <= 0:
                break
            take = min(counts[idx], remaining)
            if take > 0:
                ans = ans * pow(nums[idx], take, MOD) % MOD
                remaining -= take

        return ans
```
- Notes:
  - We compute the number of distinct prime factors using a simple sieve-like accumulation: for each prime p we increment counts for all multiples of p.
  - prev/next are computed with monotonic stacks respecting the tie-breaking rule (leftmost wins on equal prime-score).
  - Each index contributes (i - prev[i]) * (next[i] - i) subarrays where it would be chosen.
  - Sorting by nums descending and greedily taking as many selections as possible for larger values maximizes the product.
  - Time complexity: O(maxA log log maxA + n log n). Space: O(maxA + n).