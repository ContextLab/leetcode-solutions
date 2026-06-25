# [Problem 3737: Count Subarrays With Majority Element I](https://leetcode.com/problems/count-subarrays-with-majority-element-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can't provide a step-by-step stream-of-consciousness, but here's a concise summary of the initial idea: convert the array into +1 for elements equal to target and -1 for others. A subarray has target as majority iff the sum of that transformed subarray is > 0. So we need to count the number of subarrays whose sum is positive. Using prefix sums, this reduces to counting pairs (i, j) with i < j and pref[j] > pref[i]. We can count such pairs efficiently with coordinate compression + a Fenwick tree (binary indexed tree) or use merge-sort counting.

## Refining the problem, round 2 thoughts
- Construct prefix sums pref[0] = 0, pref[k] = sum of transformed values up to index k-1.
- For each prefix value in order, the number of earlier prefix values strictly smaller than the current one contributes to the answer.
- Coordinate-compress the prefix sums (since values can be negative and arbitrary) and use a Fenwick tree to maintain counts of seen prefix sums and query counts of strictly smaller ones.
- Edge cases: if target does not appear in nums, there will be no subarray with target as majority (algorithm naturally returns 0). n <= 1000 so a naive O(n^2) approach would pass, but Fenwick gives O(n log n).
- Time complexity: O(n log n) due to compression + Fenwick operations. Space: O(n).

## Attempted solution(s)
```python
from typing import List

class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, i: int, delta: int) -> None:
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def query(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

class Solution:
    def countSubarrays(self, nums: List[int], target: int) -> int:
        # Build transformed prefix sums: +1 for target, -1 otherwise
        pref = [0]
        cur = 0
        for x in nums:
            cur += 1 if x == target else -1
            pref.append(cur)

        # Coordinate compress prefix sums
        uniq = sorted(set(pref))
        comp = {v: i + 1 for i, v in enumerate(uniq)}  # 1-based indices for Fenwick

        # Fenwick to count number of previous prefix sums with value < current prefix sum
        fw = Fenwick(len(uniq))
        ans = 0
        for v in pref:
            idx = comp[v]
            # count of prefix values strictly less than current
            ans += fw.query(idx - 1)
            # mark current prefix as seen
            fw.update(idx, 1)

        return ans
```
- Solution approach: transform array elements to +1 for target and -1 otherwise; count subarrays with positive sum by counting prefix pairs pref[j] > pref[i]. Use coordinate compression and a Fenwick tree to count earlier prefix sums strictly smaller than current prefix sum.
- Time complexity: O(n log n) where n = len(nums). Coordinate compression is O(n log n) and each Fenwick operation is O(log n).
- Space complexity: O(n) for prefix sums, compression map, and Fenwick array.
- Notes: For n <= 1000 a straightforward O(n^2) double loop that checks counts also works, but the provided approach scales better and is clean to reason about.