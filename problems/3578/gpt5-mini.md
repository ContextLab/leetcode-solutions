# [Problem 3578: Count Partitions With Max-Min Difference at Most K](https://leetcode.com/problems/count-partitions-with-max-min-difference-at-most-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count ways to cut the array into contiguous segments where each segment's max - min <= k. That suggests dynamic programming: dp[i] = number of ways to partition prefix of length i. For dp[i] we sum dp[j] for all j where segment j..i-1 is valid. Naively checking all j for each i is O(n^2) and could be too slow for n up to 5e4.

Observation: for a fixed right end i-1, as j moves left the range max-min is nondecreasing (adding elements can't decrease max-min). So for each right i-1 there is a smallest j* such that any j >= j* yields a valid segment [j..i-1]. So dp[i] = sum_{j=j*..i-1} dp[j]. If we maintain prefix sums of dp, we can compute this sum in O(1) once j* is known. So the remaining challenge is to find j* quickly for each i.

We can maintain a sliding window with two monotonic deques (one for max, one for min). Move the right pointer forward; while current window [L..i] violates (max-min > k) increment L and pop expired indices from deques. L will be nondecreasing across i, giving amortized O(n). So overall O(n) time.

## Refining the problem, round 2 thoughts
Edge cases:
- dp indices and prefix sums: be careful with off-by-one. I'll use dp[0]=1 (empty prefix), dp[t] = number ways for first t elements (t from 1..n). When processing element at index i (0-based), we compute dp[i+1].
- When L==0 need to subtract zero from prefix sum.
- Maintain deques storing indices; when moving L forward pop indices equal to L from both deques.
- Use modulo 10**9+7 everywhere and ensure differences are normalized positive.

Complexity:
- Time: O(n) amortized since each index enters/pops deques at most once.
- Space: O(n) for dp/prefix arrays and O(n) worst-case for deques but deques are at most n aggregated.

## Attempted solution(s)
```python
from collections import deque

class Solution:
    def countPartitions(self, nums: list[int], k: int) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # dp[t] = number of ways to partition first t elements (t in [0..n])
        dp = [0] * (n + 1)
        pref = [0] * (n + 1)  # pref[t] = sum_{u=0..t} dp[u]
        dp[0] = 1
        pref[0] = 1

        L = 0
        maxdq = deque()  # indices with nums[...] in decreasing order
        mindq = deque()  # indices with nums[...] in increasing order

        for i in range(n):
            x = nums[i]
            # maintain monotonic deques for max and min
            while maxdq and nums[maxdq[-1]] < x:
                maxdq.pop()
            maxdq.append(i)
            while mindq and nums[mindq[-1]] > x:
                mindq.pop()
            mindq.append(i)

            # shrink from left until window [L..i] satisfies max-min <= k
            while maxdq and mindq and nums[maxdq[0]] - nums[mindq[0]] > k:
                # if the leftmost index equals L, pop it from the corresponding deque
                if maxdq and maxdq[0] == L:
                    maxdq.popleft()
                if mindq and mindq[0] == L:
                    mindq.popleft()
                L += 1

            # Now valid windows are those starting at any j in [L..i]
            left_pref = pref[L - 1] if L > 0 else 0
            dp[i + 1] = (pref[i] - left_pref) % MOD
            pref[i + 1] = (pref[i] + dp[i + 1]) % MOD

        return dp[n]
```
- Notes about the approach:
  - We use dp with prefix sums to get dp[i+1] = sum_{j=L..i} dp[j] = pref[i] - pref[L-1].
  - Two monotonic deques maintain current window's maximum and minimum in O(1) time per update; incrementing L until the window is valid moves L monotonically, giving amortized O(n) total movement.
  - Time complexity: O(n). Space complexity: O(n).
  - All arithmetic is done modulo 10^9 + 7.