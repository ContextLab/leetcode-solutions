# [Problem 3312: Sorted GCD Pair Queries](https://leetcode.com/problems/sorted-gcd-pair-queries/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to produce the sorted list of gcds for all pairs (i < j) and answer queries returning the value at a given index in that sorted list. Directly enumerating all O(n^2) pairs is impossible for n up to 1e5. Observations:
- nums[i] <= 5e4, so the set of possible gcd values is limited (1..MAXA).
- If I can count how many pairs have gcd equal to each g, I can produce a frequency histogram of gcd values and answer queries by cumulative counts (binary search).
- There's a common technique: for each divisor d, count how many numbers in nums are divisible by d => cnt[d]. Number of pairs whose gcd is divisible by d is C(cnt[d], 2). Using inclusion-exclusion over multiples (sieve-like), one can compute number of pairs whose gcd equals exactly d by subtracting contributions of multiples of d.
- So compute cnt[d] for d=1..MAXA by summing freq[m] over multiples m of d, then pairs_divisible[d] = C(cnt[d],2), then compute exact[d] by iterating d descending and subtracting exact[k*d] for k>=2.
- After exact counts computed, build prefix sums in ascending gcd order; each query q asks for the smallest gcd value with cumulative count > q.

This seems feasible: MAXA = 5e4, sum_{d=1..MAXA} MAXA/d ~ MAXA * log(MAXA) ~ a few 1e5–1e6 operations — fast.

## Refining the problem, round 2 thoughts
Edge cases & details:
- Counts can be large: number of pairs up to ~5e9, so use Python ints (unbounded) or ensure 64-bit.
- queries are 0-based indices into the sorted array; we need to find smallest g such that cumulative_count[g] > queries[i].
- Implementation detail: build arrays of length MAXA+1, with index 0 unused.
- Complexity:
  - Building cnt via multiples: O(MAXA * H_MAXA) ~ ~5e4 * ~11 = ~5.5e5 operations.
  - Computing exact by iterating multiples again: same magnitude.
  - Answering queries with binary search: O(Q log MAXA).
- Memory: arrays of size MAXA+1 (~5e4) are fine.
Alternative approaches: use Mobius transform; but sieve-like subtraction is simple and efficient here.

## Attempted solution(s)
```python
from typing import List
import bisect

class Solution:
    def minPrime(self):  # placeholder to satisfy LeetCode environment; not used
        pass

    def sortedGcd(self, nums: List[int], queries: List[int]) -> List[int]:
        # Primary solution function (keeps name similar to problem for clarity)
        MAXA = max(nums)
        n = len(nums)

        # frequency of each value
        freq = [0] * (MAXA + 1)
        for v in nums:
            freq[v] += 1

        # cnt[d] = number of elements divisible by d
        cnt = [0] * (MAXA + 1)
        for d in range(1, MAXA + 1):
            c = 0
            for m in range(d, MAXA + 1, d):
                c += freq[m]
            cnt[d] = c

        # pairs_divisible[d] = number of pairs (i<j) where both numbers divisible by d
        pairs_div = [0] * (MAXA + 1)
        for d in range(1, MAXA + 1):
            c = cnt[d]
            pairs_div[d] = c * (c - 1) // 2

        # exact[d] = number of pairs with gcd exactly d
        exact = [0] * (MAXA + 1)
        for d in range(MAXA, 0, -1):
            s = 0
            # subtract contributions from multiples of d (strictly greater than d)
            multiple = 2 * d
            while multiple <= MAXA:
                s += exact[multiple]
                multiple += d
            exact[d] = pairs_div[d] - s

        # Build cumulative counts for gcd values in ascending order
        cum = [0] * (MAXA + 1)
        running = 0
        for d in range(1, MAXA + 1):
            running += exact[d]
            cum[d] = running

        # For each query (0-based index), find smallest d with cum[d] > q
        ans = []
        for q in queries:
            # need first index with cumulative count >= q+1
            pos = bisect.bisect_left(cum, q + 1, 1, MAXA + 1)
            ans.append(pos)
        return ans

# LeetCode signature compatibility
class Solution:
    def countSortedGcdPairQueries(self, nums: List[int], queries: List[int]) -> List[int]:
        # The function called by judge will likely be sortedGcdPairQueries or similar.
        # Provide a wrapper to the implemented logic above.
        # For LeetCode submission use the standard name:
        MAXA = max(nums)
        freq = [0] * (MAXA + 1)
        for v in nums:
            freq[v] += 1

        cnt = [0] * (MAXA + 1)
        for d in range(1, MAXA + 1):
            for m in range(d, MAXA + 1, d):
                cnt[d] += freq[m]

        pairs_div = [0] * (MAXA + 1)
        for d in range(1, MAXA + 1):
            c = cnt[d]
            pairs_div[d] = c * (c - 1) // 2

        exact = [0] * (MAXA + 1)
        for d in range(MAXA, 0, -1):
            s = 0
            for m in range(2 * d, MAXA + 1, d):
                s += exact[m]
            exact[d] = pairs_div[d] - s

        cum = [0] * (MAXA + 1)
        run = 0
        for d in range(1, MAXA + 1):
            run += exact[d]
            cum[d] = run

        import bisect
        res = []
        for q in queries:
            pos = bisect.bisect_left(cum, q + 1, 1, MAXA + 1)
            res.append(pos)
        return res

# For direct LeetCode submission, the required class/method name is:
# class Solution:
#     def gcdQueries(self, nums: List[int], queries: List[int]) -> List[int]:
# Replace the wrapper name above accordingly.
```

- Notes about the approach:
  - We count for each d how many array elements are divisible by d (cnt[d]).
  - pairs_div[d] = C(cnt[d], 2) counts pairs with gcd multiple of d.
  - exact[d] is computed by inclusion-exclusion: exact[d] = pairs_div[d] - sum_{k>=2} exact[k*d]. We process d from large to small so multiples' exact counts are already known.
  - Build cumulative counts cum[d] = #pairs with gcd <= d. For a 0-based query q, answer is smallest d with cum[d] > q (binary search).
- Complexity:
  - Time: O(MAXA * (1 + 1/2 + 1/3 + ...)) ~ O(MAXA log MAXA) for the sieving steps plus O(Q log MAXA) for answering queries. With MAXA <= 5e4 this is fast.
  - Space: O(MAXA) for arrays freq, cnt, pairs_div, exact, cum.

This solution is efficient and handles large n since it avoids enumerating all pairs directly.