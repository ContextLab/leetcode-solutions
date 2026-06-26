# [Problem 3739: Count Subarrays With Majority Element II](https://leetcode.com/problems/count-subarrays-with-majority-element-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count subarrays where target appears strictly more than half the length. Naively checking all O(n^2) subarrays and counting frequencies is too slow for n up to 1e5.

A common trick for majority-like conditions is to convert elements into +1 for target and -1 for everything else. For any subarray, target is majority iff count(target) > len/2, i.e. 2*count(target) > len. If we map target->+1 and others->-1, then the sum over the subarray is count(target) - (len - count(target)) = 2*count(target) - len. So majority condition becomes subarray-sum > 0.

So the problem reduces to: count number of subarrays with sum > 0 in an array of +1/-1. That's equivalent to counting pairs of prefix sums (i < j) where pref[j] - pref[i] > 0 => pref[i] < pref[j]. So we need number of ordered pairs (i, j) with i < j and pref[i] < pref[j]. That's counting increasing pairs in the prefix array. That can be done with coordinate compression + Fenwick (BIT) or via modified merge sort counting.

## Refining the problem, round 2 thoughts
- Build prefix array pref[0] = 0, pref[k] = sum of mapped values up to index k-1. We have n+1 prefix values.
- Count number of pairs (i < j) with pref[i] < pref[j]. We must use strict < (not <=).
- Plan: compress pref values to ranks and iterate left-to-right, using a Fenwick tree counting how many previous prefixes had a smaller rank than current. For each prefix in order: query count of ranks < current_rank, add to answer; then increment current_rank count in Fenwick.
- Time complexity: O(n log n) from compression + n Fenwick ops.
- Space: O(n) for prefix + compression mapping + Fenwick.
- Edge cases: if target doesn't appear at all, then all mapped values are -1, prefixes non-increasing and answer should be 0 (algorithm naturally yields 0). Also large negative prefix values handled by compression.

## Attempted solution(s)
```python
from typing import List

class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)
    def add(self, idx: int, val: int):
        while idx <= self.n:
            self.bit[idx] += val
            idx += idx & -idx
    def sum(self, idx: int) -> int:
        res = 0
        while idx > 0:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

class Solution:
    def countSubarrays(self, nums: List[int], target: int) -> int:
        n = len(nums)
        # Build prefix sums after mapping: target -> +1, else -> -1
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i+1] = pref[i] + (1 if nums[i] == target else -1)
        # Coordinate compress prefix values
        vals = sorted(set(pref))
        rank = {v: i+1 for i, v in enumerate(vals)}  # 1-based for Fenwick
        fw = Fenwick(len(vals))
        ans = 0
        # Iterate prefixes left to right: count previous pref < current pref
        for v in pref:
            r = rank[v]
            # number of previous prefixes with rank strictly less than r
            ans += fw.sum(r - 1)
            fw.add(r, 1)
        return ans
```
- Approach: map elements to +1/-1, compute prefix sums, count ordered pairs of prefixes with pref[i] < pref[j] using coordinate compression + Fenwick tree.
- Time complexity: O(n log n) due to sorting for compression and Fenwick operations.
- Space complexity: O(n) for prefix array, compression map, and Fenwick tree.
- Implementation notes: Use strict < by querying Fenwick sum up to rank-1. The solution naturally handles the case when target is absent (answer 0). The result fits in 64-bit since max pairs is n*(n+1)/2.