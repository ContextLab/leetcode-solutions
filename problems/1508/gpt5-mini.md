# [Problem 1508: Range Sum of Sorted Subarray Sums](https://leetcode.com/problems/range-sum-of-sorted-subarray-sums/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the sum of the subarray sums in sorted order between two indices left and right (1-indexed). Naively generating all O(n^2) subarray sums and sorting them would cost O(n^2 log n^2) time and O(n^2) memory; with n up to 1000 this is borderline (about 500k sums) but would be heavy and unnecessary.

Since all nums are positive, subarray sums are strictly increasing as we extend a right pointer for a fixed left. That monotonicity suggests we can use binary search on value (a threshold T) to count how many subarray sums are <= T and also compute the total of those subarray sums. If we can get "count and sum of all subarray sums <= T" in O(n) using two pointers + prefix sums, then we can binary-search the threshold to obtain the sum of the smallest k subarray sums. With that helper we compute sum_k(right) - sum_k(left-1).

So approach: for a threshold T, use two pointers (left and right indices for subarrays) plus prefix sums and a prefix-of-prefix to compute both the count and the sum of subarray sums <= T in O(n). Then binary search for the threshold that gives at least k sums, and adjust for ties by subtracting surplus * T.

## Refining the problem, round 2 thoughts
Key details:
- Build prefix sums pref where pref[i] = sum(nums[:i]) (pref[0] = 0). Sum of subarray i..j is pref[j+1] - pref[i].
- Build pref2 where pref2[t] = sum_{u=1..t} pref[u] so that sum_{k=i..r} pref[k+1] = pref2[r+1] - pref2[i].
- For each start i, find the largest r >= i with pref[r+1] - pref[i] <= T. Count adds (r - i + 1), sum adds (pref2[r+1] - pref2[i]) - (r - i + 1) * pref[i].
- Use a monotonic r (two-pointer) so total O(n) for one threshold.
- Binary search T over [1, total_sum] to find smallest T with count >= k.
- sum_k(k): find threshold T, get (cnt, total_sum_leq_T), then subtract (cnt - k) * T (since among sums equal to T we only want k).
- Final answer is (sum_k(right) - sum_k(left-1)) % MOD.

Complexities:
- Each count/sum check: O(n).
- Binary search over T up to sum(nums) which is <= 100*1000 = 100k, so about log2(1e5) ~ 17 iterations. So overall time O(n log S) where S = total sum. With n <= 1000 this is fine.
- Space O(n) for prefix arrays.

Edge cases:
- k = 0 -> return 0.
- Use Python ints (big) and only apply modulo at the end.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def rangeSum(self, nums: List[int], n: int, left: int, right: int) -> int:
        MOD = 10**9 + 7

        # Build prefix sums
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i+1] = pref[i] + nums[i]
        # pref2[t] = sum_{u=1..t} pref[u]
        pref2 = [0] * (n + 1)
        for t in range(1, n+1):
            pref2[t] = pref2[t-1] + pref[t]

        # Given threshold T, return (count of subarray sums <= T, total sum of those subarray sums)
        def count_and_sum_leq(T: int):
            cnt = 0
            total = 0
            r = -1
            # iterate over start i
            for i in range(n):
                # ensure r is at least i-1 (monotonic)
                if r < i - 1:
                    r = i - 1
                # try to expand r while subarray sum i..(r+1) <= T
                # sum(i..x) = pref[x+1] - pref[i]
                while r + 1 < n and pref[r+2] - pref[i] <= T:
                    r += 1
                if r >= i:
                    cnt_here = r - i + 1
                    # sum of pref[k+1] for k=i..r is pref2[r+1] - pref2[i]
                    sum_prefs = pref2[r+1] - pref2[i]
                    # subtract cnt_here * pref[i] to get actual sums of subarrays i..k
                    total_here = sum_prefs - cnt_here * pref[i]
                    cnt += cnt_here
                    total += total_here
            return cnt, total

        # sum of smallest k subarray sums
        def sum_k(k: int) -> int:
            if k <= 0:
                return 0
            lo, hi = 1, pref[-1]  # possible subarray sums range (positive nums)
            while lo < hi:
                mid = (lo + hi) // 2
                cnt, _ = count_and_sum_leq(mid)
                if cnt >= k:
                    hi = mid
                else:
                    lo = mid + 1
            T = lo
            cnt, total = count_and_sum_leq(T)
            # If there are more than k sums <= T, we overcounted (they include some sums equal to T).
            surplus = cnt - k
            if surplus > 0:
                total -= surplus * T
            return total

        ans = (sum_k(right) - sum_k(left - 1)) % MOD
        return ans
```
- Notes:
  - The helper count_and_sum_leq uses a monotonic two-pointer r and precomputed prefix-of-prefix (pref2) to compute the sum of all subarray sums starting at i and ending at <= r in O(1) per i.
  - Binary search finds the minimal threshold T such that at least k subarray sums are <= T; then we adjust the total to account for ties equal to T.
  - Time complexity: O(n * log S) where S = sum(nums) (S <= 100000 here). With n <= 1000 this is efficient. Space complexity: O(n) for prefix arrays.
  - Use modulo only at the final answer to avoid interfering with comparisons during binary search.